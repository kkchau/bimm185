import gzip
import pymysql
import getpass
import re
from pymysql import cursors
from Bio import SeqIO as sio


# global variables
genome_table_col = ['genome_id', 'name', 'tax_id', 'domain', 'num_replicons', 'num_genes', 'size_bp', 'assembly']
rep_table_col = ['replicon_id', 'genome_id', 'name', 'type', 'shape', 'num_genes', 'size_bp', 'accession', 'release_date']
gene_table_col = ['gene_id', 'genome_id', 'replicon_id', 'locus_tag', 'protein_id', 'name', 'strand', 'num_exons', 'length', 'product']
ex_ref_table_col = ['gene_id', 'xdb', 'xid']
exons = ['gene_id', 'exon', 'l_position', 'r_position', 'length']
syn = ['gene_id', 'synonym']
functions = ['gene_id', 'function']

genome_id = 0
replicon_id = 0
gene_id = 0
exon_id = 0


def sqlInsert(sql_connection, table, col_list, values):
    """
        Execute INSERT command to the given SQL connection.
    """

    with sql_connection.cursor() as cursor:
        sub_set = ','.join(['%s' for _ in range(len(values))])
        command = "INSERT INTO " + table + "(" + ','.join(col_list) + ") VALUES (" + sub_set + ");"
        cursor.execute(command, values)

    sql_connection.commit()

    return 0        # return code


def populate_tables(filename, connection):
    """
        Insert relevant information to SQL tables
    """
    with gzip.open(filename, 'rt') as gbff:

        global genome_id
        global replicon_id
        global gene_id
        global exon_id

        genome_id += 1                  # genome identifier increment
        num_rep = 0                     # number of replicons for this genome
        tot_genes = 0                   # total number of genes for this genome
        full_length = 0                 # length of this genome
        assembly = ''                   # assembly variable

        # iterate through all the records in the gb file (replicons)
        for record in sio.parse(gbff, 'genbank'):

            replicon_id += 1            # increment replicon identifier
            num_rep += 1                # increment number of replicons
            rep_genes = 0               # counter for replicon genes
            rep_size = 0                # size of replicon

            # record annotations are stored in dictionary format
            domain = record.annotations['taxonomy'][0]
            accession = ','.join(record.annotations['accessions'])
            release_date = record.annotations['date']
            assembly = [str(ref.strip().split(':')[1]) for ref in record.dbxrefs
                        if 'Assembly' in ref]

            # replicon information
            name = record.annotations['organism']
            rep_name = record.description
            topology = record.annotations['topology']
            rep_type = 'plasmid' if 'plasmid' in record.description else 'chromosome'

            # features (e.g. CDS)
            for feature in record.features:

                # pull information from source feature
                if feature.type == 'source':
                    #print(feature)
                    tax_id = ','.join(feature.qualifiers.get('db_xref')).strip().split(':')[1]
                    rep_size = int(re.findall("([0-9]+)", str(feature.location.end))[0])
                    full_length += rep_size

                # gene information
                elif feature.type == 'CDS':

                    # skip pseudogenes
                    if feature.qualifiers.get('pseudo') is not None:
                        continue

                    # skip incomplete genes
                    if '<' in str(feature.location.start):
                        continue
                    if '>' in str(feature.location.end):
                        continue

                    # get strand
                    strand = 'F' if feature.location.strand > 0 else 'R'

                    # get gene start and end
                    start = re.findall("([0-9]+)", str(feature.location.start))[0]
                    end = re.findall("([0-9]+)", str(feature.location.end))[0]

                    rep_genes += 1          # replicon gene counter
                    gene_id += 1            # gene identifier

                    print(feature)

                    # gene name if available
                    if feature.qualifiers.get('gene'):
                        gene_name = feature.qualifiers.get('gene')
                    else:
                        gene_name = feature.qualifiers.get('locus_tag')[0]

                    # get locus tag
                    locus_tag = feature.qualifiers.get('locus_tag')[0]
                    g_length = int(end) - int(start)
                    product = feature.qualifiers.get('product')

                    # protein_id
                    if feature.qualifiers.get('protein_id'):
                        protein_id = str(str(feature.qualifiers.get('protein_id')[0]).strip().split('.')[0])

                        # protein_id is also an external reference
                        sqlInsert(connection, 'gene_xrefs', ex_ref_table_col, [gene_id, 'refseq', protein_id])

                    else:
                        protein_id = '-'

                    # insert gene
                    sqlInsert(connection, 'genes', gene_table_col, [gene_id, genome_id, replicon_id, locus_tag, protein_id, gene_name, strand, 1, g_length, product])

                    # external references
                    if feature.qualifiers.get('db_xref'):
                        for xr in feature.qualifiers.get('db_xref'):
                            db = xr.strip().split(':')[0]
                            ref = xr.strip().split(':')[1]
                            sqlInsert(connection, 'gene_xrefs', ex_ref_table_col, [gene_id, db, ref])

                    # exon information
                    for loc in feature.location.parts:
                        exon_id += 1
                        ex_start = int(loc.start)
                        ex_end = int(loc.end)
                        sqlInsert(connection, 'exons', exons, [gene_id, exon_id, ex_start, ex_end, ex_end - ex_start])

                    # synonyms
                    if feature.qualifiers.get('gene_synonym'):
                        for s in feature.qualifiers.get('gene_synonym')[0].strip().split(';'):
                            sqlInsert(connection, 'gene_synonyms', syn, [gene_id, s])

                    # functions
                    if feature.qualifiers.get('function'):
                        for f in feature.qualifiers.get('function'):
                            sqlInsert(connection, 'functions', functions, [gene_id, f])

            # replicons table entry
            rep_table_info = [replicon_id, genome_id, record.description, rep_type, topology, rep_genes, rep_size, accession, release_date]
            sqlInsert(connection, 'replicons', rep_table_col, rep_table_info)
            tot_genes += rep_genes

        genome_table_info = [genome_id, name, tax_id, domain, num_rep, tot_genes, full_length, assembly]

        # genomes table entry
        sqlInsert(connection, 'genomes', genome_table_col, genome_table_info)

        return 0


if __name__ == '__main__':

    print("Connecting to bm185s-mysql.ucsd.edu as kkchau; using kkchau_db")
    passwd = getpass.getpass("Input password: ")

    # create connection to database
    sqlconnection = pymysql.connect(host='bm185s-mysql.ucsd.edu',
                                    user='kkchau',
                                    password=str(passwd),
                                    db='kkchau_db',
                                    cursorclass=pymysql.cursors.DictCursor)

    e_coli = '/home/linux/ieng6/bm185s/kkchau/bimm185/week4/genomes/e_coli/GCF_000005845.2_ASM584v2_genomic.gbff.gz'
    a_tuma = '/home/linux/ieng6/bm185s/kkchau/bimm185/week4/genomes/a_tumafaciens/GCF_000576515.1_ASM57651v1_genomic.gbff.gz'

    populate_tables(e_coli, sqlconnection)
    populate_tables(a_tuma, sqlconnection)

    sqlconnection.close()

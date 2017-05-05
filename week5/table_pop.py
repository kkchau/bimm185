import gzip
import pymysql
import getpass
import re
from pymysql import cursors
from Bio import SeqIO as sio


# define mysql functions so I don't have to type everything out all of the time
def sqlInsert(sql_connection, table, col_list, values):
    with sql_connection.cursor() as cursor:
        sub_set = ','.join(['%s' for _ in range(len(values))])
        command = "INSERT INTO " + table + "(" + ','.join(col_list) + ") VALUES (" + sub_set + ");"
        cursor.execute(command, values)

    sql_connection.commit()

    return 0        # return code


genome_table_col = ['genome_id', 'name', 'tax_id', 'domain', 'num_replicons', 'num_genes', 'size_bp', 'assembly']
rep_table_col = ['replicon_id', 'genome_id', 'name', 'type', 'shape', 'num_genes', 'size_bp', 'accession', 'release_date']
gene_table_col = ['gene_id', 'genome_id', 'replicon_id', 'locus_tag', 'protein_id', 'name', 'strand', 'num_exons', 'length', 'product']
ex_ref_table_col = ['gene_id', 'xdb', 'xid']
exons = ['gene_id', 'exon', 'l_position', 'r_position', 'length']
syn = ['gene_id', 'synonym']
functions = ['gene_id', 'function']


def populate_tables(filename, gen_id, rep_id, gene_id, ex_id, assembly, connection):
    with gzip.open(filename, 'rt') as gbff:

        gen_id += 1
        gene_counter = 0
        num_rep = 0
        tot_genes = 0
        full_length = 0

        # iterate through all the records in the gb file (replicons)
        for record in sio.parse(gbff, 'genbank'):

            rep_id += 1
            num_rep += 1
            rep_genes = 0
            rep_size = 0
            rep_type = 'plasmid' if 'plasmid' in record.description else 'chromosome'

            # record annotations are stored in dictionary format
            domain = record.annotations['taxonomy'][0]
            accession = ','.join(record.annotations['accessions'])
            release_date = record.annotations['date']

            # replicon information
            rep_name = record.annotations['organism']
            topology = record.annotations['topology']

            # features (e.g. CDS)
            for feature in record.features:

                # pull information from source feature
                if feature.type == 'source':
                    #print(feature)
                    tax_id = ','.join(feature.qualifiers.get('db_xref')).strip().split(':')[1]
                    bp_size = re.findall("([0-9]+)", str(feature.location.end))[0]
                    full_length += int(bp_size)
                    rep_size = int(bp_size)

                # gene information
                elif feature.type == 'CDS':
                    if feature.qualifiers.get('note'):
                        if 'pseudo' in feature.qualifiers.get('note')[0]:
                            continue
                    if feature.qualifiers.get('pseudo') is not None:
                        continue
                    rep_genes += 1
                    gene_id += 1
                    print(feature)
                    if feature.qualifiers.get('name'):
                        gene_name = feature.qualifiers.get('name')
                    else:
                        gene_name = feature.qualifiers.get('locus_tag')[0]
                    locus_tag = feature.qualifiers.get('locus_tag')[0]
                    strand = 'F' if feature.location.strand > 0 else 'R'
                    start = re.findall("([0-9]+)", str(feature.location.start))[0]
                    end = re.findall("([0-9]+)", str(feature.location.end))[0]
                    g_length = int(end) - int(start)
                    product = feature.qualifiers.get('product')
                    if feature.qualifiers.get('protein_id'):
                        protein_id = str(str(feature.qualifiers.get('protein_id')[0]).strip().split('.')[0])
                    else:
                        protein_id = '-'

                    # insert gene
                    sqlInsert(connection, 'genes', gene_table_col, [gene_id, gen_id, rep_id, locus_tag, protein_id, gene_name, strand, 1, g_length, product])

                    # external references
                    if feature.qualifiers.get('db_xref'):
                        for xr in feature.qualifiers.get('db_xref'):
                            db = xr.strip().split(':')[0]
                            ref = xr.strip().split(':')[1]
                            sqlInsert(connection, 'gene_xrefs', ex_ref_table_col, [gene_id, db, ref])

                    # exon information
                    ex_id += 1
                    sqlInsert(connection, 'exons', exons, [gene_id, ex_id, start, end, g_length])

                    # synonyms
                    if feature.qualifiers.get('gene_synonym'):
                        for s in feature.qualifiers.get('gene_synonym'):
                            sqlInsert(connection, 'gene_synonyms', syn, [gene_id, s])

                    if feature.qualifiers.get('function'):
                        for f in feature.qualifiers.get('function'):
                            sqlInsert(connection, 'functions', functions, [gene_id, f])

            # replicons table entry
            rep_table_info = [rep_id, gen_id, record.description, rep_type, topology, rep_genes, rep_size, accession, release_date]
            sqlInsert(connection, 'replicons', rep_table_col, rep_table_info)
            tot_genes += rep_genes

        genome_table_info = [gen_id, rep_name, tax_id, domain, num_rep, tot_genes, full_length, assembly]

        # genomes table entry
        sqlInsert(connection, 'genomes', genome_table_col, genome_table_info)

        return gen_id, rep_id, gene_id, ex_id


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

    gid = 0
    rid = 0
    geid = 0
    eid = 0
    gid, rid, geid, eid = populate_tables(e_coli, gid, rid, geid, eid, 'GCF_000005845.2', sqlconnection)
    gid, rid, geid, eid = populate_tables(a_tuma, gid, rid, geid, eid, 'GCF_000576515.1', sqlconnection)

    sqlconnection.close()

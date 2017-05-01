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

    connection.commit()

    return 0        # return code


print("Connecting to bm185s-mysql.ucsd.edu as kkchau; using kkchau_db")
passwd = getpass.getpass("Input password: ")

# create connection to database
connection = pymysql.connect(host='bm185s-mysql.ucsd.edu',
                             user='kkchau',
                             password=str(passwd),
                             db='kkchau_db',
                             cursorclass=pymysql.cursors.DictCursor)


genome_table_col = ['tax_id', 'gen_short_name', 'gen_long_name', 'bp_size', 'domain', 'accession', 'release_date']
rep_table_col = ['replicon_id', 'genome_id', 'name', 'CDS', 'rep_type', 'rep_structure']
gene_table_col = ['gene_id', 'genome_id', 'replicon_id', 'locus_tag', 'name', 'strand', 'num_exons', 'length', 'product_name']
exons_table_col = ['gene_id', 'exon', 'l_position', 'r_position', 'length']
synonyms_table_col = ['gene_id', 'synonym']
ex_ref_table_col = ['gene_id', 'external_db', 'external_id']
func_table_col = ['gene_id', 'function']

gen_id = 0
rep_id = 0

# e_coli information
with gzip.open('/home/linux/ieng6/bm185s/kkchau/bimm185/week4/genomes/e_coli/GCF_000005845.2_ASM584v2_genomic.gbff.gz', 'rt') as gbff:

    gen_id += 1
    full_length = 0
    
    # iterate through all the records in the gb file (replicons)
    for record in sio.parse(gbff, 'genbank'):

        rep_id += 1
        num_gene = 0
        rep_type = 'plasmid'

        # record annotations are stored in dictionary format
        domain = record.annotations['taxonomy'][0]
        accession = ','.join(record.annotations['accessions'])
        release_date = record.annotations['date']

        # replicon information
        rep_name = record.annotations['organism']
        topology = record.annotations['topology']

        for feature in record.features:
            
            # pull information from source feature
            if feature.type == 'source':
                #print(feature)
                tax_id = ','.join(feature.qualifiers.get('db_xref')).strip().split(':')[1]
                gen_short_name = ','.join(feature.qualifiers.get('organism')).strip().split()
                gen_short_name = gen_short_name[0][:1]  + '. ' + gen_short_name[1]
                gen_long_name = ','.join(feature.qualifiers.get('organism'))
                bp_size = re.findall("([0-9]+)", str(feature.location.end))[0]
                full_length += int(bp_size)

            elif feature.type == 'CDS':
                num_gene += 1
                print(feature)
                if feature.qualifiers.get('gene'):
                    gene_id = feature.qualifiers.get('gene')[0]
                else:
                    gene_id = '-'
                locus_tag = feature.qualifiers.get('locus_tag')[0]
                strand = '+' if feature.location.strand > 0 else '-'
                start = re.findall("([0-9]+)", str(feature.location.start))[0]
                end = re.findall("([0-9]+)", str(feature.location.end))[0]
                g_length = int(end) - int(start)
                product = feature.qualifiers.get('product')

                sqlInsert(connection, 'genes', gene_table_col, [gene_id, gen_id, rep_id, locus_tag, rep_name, strand, 1, g_length, product])

                # exons table
                sqlInsert(connection, 'exons', exons_table_col, [gene_id, 1, start, end, g_length])

                # synonyms table
                if feature.qualifiers.get('gene_synonym'):
                    for syn in feature.qualifiers.get('gene_synonym')[0].strip().split(';'):
                        sqlInsert(connection, 'gene_synonyms', synonyms_table_col, [gene_id, syn])

                # external references
                if feature.qualifiers.get('db_xref'):
                    for xr in feature.qualifiers.get('db_xref'):
                        db = xr.strip().split(':')[0]
                        ref = xr.strip().split(':')[1]
                        sqlInsert(connection, 'ex_ref', ex_ref_table_col, [gene_id, db, ref])

                # functions
                if feature.qualifiers.get('function'):
                    for func in feature.qualifiers.get('function')[0].strip().split(';'):
                        sqlInsert(connection, 'functions', func_table_col, [gene_id, func])


        # replicons table entry
        rep_table_info = [rep_id, gen_id, rep_name, num_gene, rep_type, topology]
        sqlInsert(connection, 'replicons', rep_table_col, rep_table_info)

    genome_table_info = [tax_id, gen_short_name, gen_long_name, full_length, domain, accession, release_date]

    # genomes table entry
    sqlInsert(connection, 'genomes', genome_table_col, genome_table_info)


# a_tumafaciens
with gzip.open('/home/linux/ieng6/bm185s/kkchau/bimm185/week4/genomes/a_tumafaciens/GCF_000576515.1_ASM57651v1_genomic.gbff.gz', 'rt') as gbff:

    gen_id += 1
    full_length = 0
    
    # iterate through all the records in the gb file (replicons)
    for record in sio.parse(gbff, 'genbank'):

        rep_id += 1
        num_gene = 0
        rep_type = 'plasmid' if 'plasmid' in record.description else 'chromosome'

        # record annotations are stored in dictionary format
        domain = record.annotations['taxonomy'][0]
        accession = ','.join(record.annotations['accessions'])
        release_date = record.annotations['date']

        # replicon information
        rep_name = record.annotations['organism']
        topology = record.annotations['topology']

        for feature in record.features:
            
            # pull information from source feature
            if feature.type == 'source':
                #print(feature)
                tax_id = ','.join(feature.qualifiers.get('db_xref')).strip().split(':')[1]
                gen_short_name = ','.join(feature.qualifiers.get('organism')).strip().split()
                gen_short_name = gen_short_name[0][:1]  + '. ' + gen_short_name[1]
                gen_long_name = ','.join(feature.qualifiers.get('organism'))
                bp_size = re.findall("([0-9]+)", str(feature.location.end))[0]
                full_length += int(bp_size)

            elif feature.type == 'CDS':
                num_gene += 1
                print(feature)
                if feature.qualifiers.get('gene'):
                    gene_id = feature.qualifiers.get('gene')[0]
                else:
                    gene_id = '-'
                locus_tag = feature.qualifiers.get('locus_tag')[0]
                strand = '+' if feature.location.strand > 0 else '-'
                start = re.findall("([0-9]+)", str(feature.location.start))[0]
                end = re.findall("([0-9]+)", str(feature.location.end))[0]
                g_length = int(end) - int(start)
                product = feature.qualifiers.get('product')

                sqlInsert(connection, 'genes', gene_table_col, [gene_id, gen_id, rep_id, locus_tag, rep_name, strand, 1, g_length, product])

                # exons table
                sqlInsert(connection, 'exons', exons_table_col, [gene_id, 1, start, end, g_length])

                # synonyms table
                if feature.qualifiers.get('gene_synonym'):
                    for syn in feature.qualifiers.get('gene_synonym')[0].strip().split(';'):
                        sqlInsert(connection, 'gene_synonyms', synonyms_table_col, [gene_id, syn])

                # external references
                if feature.qualifiers.get('db_xref'):
                    for xr in feature.qualifiers.get('db_xref'):
                        db = xr.strip().split(':')[0]
                        ref = xr.strip().split(':')[1]
                        sqlInsert(connection, 'ex_ref', ex_ref_table_col, [gene_id, db, ref])

                # functions
                if feature.qualifiers.get('function'):
                    for func in feature.qualifiers.get('function')[0].strip().split(';'):
                        sqlInsert(connection, 'functions', func_table_col, [gene_id, func])


        # replicons table entry
        rep_table_info = [rep_id, gen_id, rep_name, num_gene, rep_type, topology]
        sqlInsert(connection, 'replicons', rep_table_col, rep_table_info)

    genome_table_info = [tax_id, gen_short_name, gen_long_name, full_length, domain, accession, release_date]

    # genomes table entry
    sqlInsert(connection, 'genomes', genome_table_col, genome_table_info)

connection.close()

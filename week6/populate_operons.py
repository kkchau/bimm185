"""
    Populate the operons table based on information found 
        in ./SampleFiles/OperonSet.txt                                         
"""


import pymysql
import subprocess
import getpass


# open sql connection
sqlconn = pymysql.connect(host='bm185s-mysql.ucsd.edu', user='kkchau',
                          passwd=getpass.getpass("Input password: "), db='kkchau_db')


# populate operons table just from OperonSet.txt
# all operons that are strong or confirmed
operons_lines = subprocess.check_output(['grep', "^[^#]", './SampleFiles/OperonSet.txt']
                                       ).splitlines()

operons_lines = [line.decode('ascii') for line in operons_lines]

for line in operons_lines:
    line = line.strip().split()

    # only strong or confirmed operons
    if 'Strong' in line[len(line) - 1] or 'Confirmed' in line[len(line) - 1]:
        genes = line[5].strip().split(',')

        # for each gene member of the operon
        for g in genes:

            # work with gene synonyms in case the gene is not in the genes table
            all_syns = [g]
            with sqlconn.cursor() as cur:
                cur.execute("SELECT gene_id FROM gene_synonyms WHERE synonym='{}'".format(g))
                g_id = cur.fetchone()
                if g_id:
                    g_id = g_id[0]
                    cur.execute("SELECT synonym FROM gene_synonyms WHERE gene_id='{}'".format(g_id))
                    g_syns = cur.fetchall()
                    all_syns.extend([synonym[0] for synonym in g_syns])

            # for each gene and its synonym
            for s in all_syns:
                with sqlconn.cursor() as cur:

                    # get the gene_id
                    cur.execute("SELECT gene_id FROM genes where name=\"{}\";".format(s))
                    result = cur.fetchone()

                    # skip if gene is not found
                    if not result:
                        break

                    # insert gene with operon
                    operon = '\"' + line[0] + '\"'
                    conf = '\"' + line[-1] + '\"'
                    cur.execute("INSERT INTO operons VALUES ({});".format(','.join([str(result[0]),operon,conf])))

                    sqlconn.commit()

sqlconn.close()

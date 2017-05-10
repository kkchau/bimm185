"""
    Get homology of specified genomes
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pymysql
from pyql import sqlConnect
from pyql import sqlInsert
from pyql import sqlSelect


connection = sqlConnect('bm185s-mysql.ucsd.edu', 'kkchau', 'kkchau_db')

# a_tumefaciens vs e_coli
q_fields, query_prot = sqlSelect(connection, 'blast_gid1', fields=['qseqid'])

# format queries
query_prot = [q for subqs in query_prot for q in subqs]
query_prot = list(set(query_prot))

# store best hits for a_tumafaciens against e_coli
first_direction = {}
for qseq1 in query_prot:
    with connection.cursor() as cursor:
        cursor.execute("SELECT sseqid FROM blast_gid1"
                       + " WHERE qseqid='{}' ".format(qseq1)
                       + "ORDER BY bitscore DESC LIMIT 1;")

    first_direction[cursor.fetchone()['sseqid'].strip().split('|')[1]] = qseq1

# perform comparison from one direction to the other
for query in first_direction:
    with connection.cursor() as cursor:
        cursor.execute("SELECT sseqid FROM blast_gid2"
                       + " WHERE qseqid='{}' ".format(query)
                       + "ORDER BY bitscore DESC LIMIT 1;")
        second_dir_match = cursor.fetchone()

        # query not even in table, skip
        if not second_dir_match:
            continue
        else:
            # formatting
            second_dir_match = second_dir_match['sseqid'].strip().split('|')[1]
        
        # if bi-directional best hit, output
        if first_direction[query] == second_dir_match:
            print("{}\t{}\t{}\t{}".format(query,
                                          second_dir_match, 
                                          'orthology', 
                                          'BDBH'))

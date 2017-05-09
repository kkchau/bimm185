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
q_fields, query_prot = sqlSelect(connection, 'blast_gid1', fields=['qseqid'])

query_prot = [q for subqs in query_prot for q in subqs]

query_prot = list(set(query_prot))

first_direction = {}

for qseq1 in query_prot:
    with connection.cursor() as cursor:
        cursor.execute("SELECT sseqid FROM blast_gid1"
                       + " WHERE qseqid='{}' ".format(qseq1)
                       + "ORDER BY bitscore DESC LIMIT 1;")

    first_direction[cursor.fetchone()['sseqid'].strip().split('|')[1]] = qseq1

for k in first_direction:
    print(k, first_direction[k])

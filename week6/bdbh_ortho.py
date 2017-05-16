"""
    Get homology of specified genomes
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pymysql
from collections import defaultdict
from pyql import sqlConnect
from pyql import sqlInsert
from pyql import sqlSelect


connection = sqlConnect('bm185s-mysql.ucsd.edu', 'kkchau', 'kkchau_db')

# a_tumefaciens vs e_coli
q_fields, query_prot = sqlSelect(connection, 'blast_gid2', fields=['qseqid'])

# format queries
query_prot = [q for subqs in query_prot for q in subqs]
query_prot = list(set(query_prot))

# store best hits for a_tumafaciens against e_coli
first_direction = defaultdict(list)
for qseq1 in query_prot:
    with connection.cursor() as cursor:
        
        # get max bitscore
        cursor.execute("SELECT bitscore FROM blast_gid2"
                       + " WHERE qseqid='{}' ".format(qseq1)
                       + "ORDER BY bitscore DESC LIMIT 1;")

        # use hard-threshold of delta(3) to get similar scores
        thresh = float(cursor.fetchone()['bitscore']) - 3
        

        # get all alignments within threshold and with at least 60% coverage
        cursor.execute("SELECT sseqid FROM blast_gid2 "
                       + "WHERE qseqid='{}' and bitscore>={} ".format(qseq1, thresh)
                       + "and qcovs>=0.6 and scov>=0.6 "
                       + "ORDER BY bitscore DESC;")

        for result in cursor.fetchall():
            first_direction[qseq1].append(
                result['sseqid'].strip().split('|')[1]
            )

# e_coli vs a_tumefaciens
query_prot = sqlSelect(connection, 'blast_gid1', fields=['qseqid'])[1]
query_prot = list(set([q for subqs in query_prot for q in subqs]))

# get best scoring hits from e_coli to a_tumefaciens
second_direction = defaultdict(list)
for qseq2 in query_prot:
    with connection.cursor() as cursor:
        
        # max bit score
        cursor.execute("SELECT bitscore FROM blast_gid1"
                       + " WHERE qseqid='{}'".format(qseq2)
                       + " ORDER BY bitscore DESC LIMIT 1;")

        # hard-threshold delta(3)
        thresh = float(cursor.fetchone()['bitscore']) - 3

        # get all alignments within threshold and with at least 60% coverage
        cursor.execute("SELECT sseqid FROM blast_gid1"
                       + " WHERE qseqid='{}' and bitscore>={}".format(qseq2, thresh)
                       + " and qcovs>=0.6 and scov>=0.6"
                       + " ORDER BY bitscore DESC;")

        for result in cursor.fetchall():
            second_direction[qseq2].append(
                result['sseqid'].strip().split('|')[1]
            )
# get all pairs that appear in each other's best-hit sets
with connection.cursor() as cursor:
    for q in first_direction:
        for s in first_direction[q]:
            if q in second_direction[s]:
                print(q, s)
                command = "INSERT INTO homology_1(seqid_1,seqid_2,h_type,method) VALUES (%s,%s,%s,%s)"
                cursor.execute(command, (s, q, 'Orthology', 'BDBH'))
                connection.commit()

connection.close()


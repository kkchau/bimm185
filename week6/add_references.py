"""
    Add external references for genes in ./SampleFiles/
    Create table linkages to consolidate references and ids from
        RegulonDB
"""


import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import subprocess
import re
from pyql import sqlConnect
from pyql import sqlSelect
from pyql import sqlInsert


# get all genes from geneproductset file
regulon_genes = {entry[2]: entry[0]
                 for entry in [g.decode('ascii').strip().split()
                 for g in subprocess.check_output(["grep", "ECK*", "./SampleFiles/GeneProductSet.txt"]).splitlines()]
                 if len(entry) > 2}

# sql connection
connection = sqlConnect('bm185s-mysql.ucsd.edu', 'kkchau', 'kkchau_db')

# for each gene in the genes table, get the gene_id, then annotate if there is
# a regulon entry
for gene in regulon_genes:
    gene = re.findall("([a-zA-Z0-9]+)", gene)[0]
    _, gene_id = sqlSelect(connection, 'genes',
                           fields=['gene_id'],
                           where='locus_tag=\'{}\''.format(gene))

    # if gene_id is found, add regulondb info to external references
    if gene_id:
        gene_id = gene_id[0][0]
        print(gene_id)
        sqlInsert(connection, 'gene_xrefs', ['gene_id', 'xdb', 'xid'],
                  [gene_id, 'RegulonDB', regulon_genes[gene]])

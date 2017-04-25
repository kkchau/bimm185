import gzip
from Bio import SwissProt as sws

# open input and output files
with gzip.open('./archaea/uniprot_sprot_archaea.dat.gz', 'rt') as arch:
    with open('./archaea/uniprot_tax.txt', 'w') as tax:

        # header
        tax.write('\t'.join(['NCBI_tax_id', 'Organism', 'Taxonomy']) + '\n')

        # write appropriate information for each record
        for record in sws.parse(arch):
            print(record.organism)
            tax.write('\t'.join([record.taxonomy_id[0], record.organism, ','.join(record.organism_classification)]) + '\n')

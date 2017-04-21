import os
import gzip
import re
from Bio import SeqIO as sio

with open('e_coli_parsed.out', 'w') as output:
    output.write('\t'.join(['accession', 'coordinates', 'strand', 'gene_name', 'locus', 'synonyms', 'protein_name', 'tax_id', 'EC_numbers', 'external_refs']) + '\n')

with gzip.open('./all_genomes/E_coli_K12_MG1655/GCF_000005845.2_ASM584v2_genomic.gbff.gz', mode='rt') as gbank:

    for record in sio.parse(gbank, 'genbank'):
        for feature in record.features:

            if feature.type == 'source':
                org = feature.qualifiers.get('organism')[0]
                tax = feature.qualifiers.get('db_xref')[0]
                tax = tax.strip().split(':')[1]

            if feature.type != 'CDS':
                continue

            print(feature)

            cds_info = []

            # protein_id
            if feature.qualifiers.get('protein_id'):
                cds_info.append(','.join(feature.qualifiers.get('protein_id')))
            else:
                cds_info.append('PSEUDO')

            # cds coordinates and strand
            loc = feature.location
            coord = '[' + str(loc.start) + ':' + str(loc.end) + ']'
            cds_info.append(coord)
            if loc.strand > 0:
                cds_info.append('+')
            elif loc.strand < 0:
                cds_info.append('-')
            else:
                cds_info.append('NONE')

            # gene name
            cds_info.append(','.join(feature.qualifiers.get('gene')))

            # locus
            cds_info.append(','.join(feature.qualifiers.get('locus_tag')))

            # synonyms
            cds_info.append(','.join(feature.qualifiers.get('gene_synonym')))

            # protein name
            if feature.qualifiers.get('product'):
                cds_info.append(','.join(feature.qualifiers.get('product')))
            else:
                cds_info.append('-')

            # tax id
            cds_info.append(org + ':' + tax)

            # EC
            if feature.qualifiers.get('EC_number'):
                cds_info.append(','.join(feature.qualifiers.get('EC_number')))
            else:
                cds_info.append('-')

            # external refs
            if feature.qualifiers.get('db_xref'):
                cds_info.append(','.join(feature.qualifiers.get('db_xref')))
            else:
                cds_info.append('-')

            print(cds_info)

            with open('e_coli_parsed.out', 'a') as output:
                output.write('\t'.join(cds_info) + '\n')

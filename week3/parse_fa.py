import gzip
from Bio import SeqIO as sio


# open file
with gzip.open('./all_genomes/E_coli_K12_MG1655/GCF_000005845.2_ASM584v2_protein.faa.gz', 'rt') as fasta:
    with open('e_coli_seq.out', 'w') as output:
        output.write('accession\tsequence\n')

        # get id and sequence, write to output
        for record in sio.parse(fasta, 'fasta'):
                output.write('{}\t{}\n'.format(record.id, str(record.seq)))

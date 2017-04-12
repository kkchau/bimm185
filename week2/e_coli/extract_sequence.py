import os

comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

full_seq = ''

with open('GCF_000005845.2_ASM584v2_genomic.fna', 'r') as sequence_file:
    next(sequence_file)
    for line in sequence_file:
        full_seq += line.strip()

fasta = {}

with open('ProteinTable167_161521.txt', 'r') as proteins:
    next(proteins)
    for line in proteins:
        line = line.strip().split()
        replicon = line[8]
        strand = line[4]
        locus = line[6]
        geneid = line[7]
        start = int(line[2]) - 1
        end = int(line[3])
        sequence = full_seq[start:end]
        if strand == '-':
            sequence = list(sequence)[::-1]
            for i, c in enumerate(sequence):
                sequence[i] = comp[c]
            sequence = ''.join(sequence)
        print(sequence)
        with open('e_coli.faa', 'a') as fasta:
            fasta.write('>')
            fasta.write('|'.join([replicon, locus, geneid]))
            for counter, character in enumerate(sequence):
                if counter % 70 == 0:
                    fasta.write('\n')
                fasta.write(character)
            fasta.write('\n')


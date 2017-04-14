import os

# complement dictionary 
comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

# store full sequence
full_seq = ''   
with open('GCF_000005845.2_ASM584v2_genomic.fna', 'r') as sequence_file:
    next(sequence_file)
    for line in sequence_file:
        full_seq += line.strip()

fasta = {}          # store id: sequence
with open('ProteinTable167_161521.txt', 'r') as proteins:
    next(proteins)  # skip header
    for line in proteins:

        # get gene information for each protein and corresponding sequence
        line = line.strip().split()
        replicon = line[8]
        strand = line[4]
        locus = line[6]
        geneid = line[7]
        start = int(line[2]) - 1
        end = int(line[3])
        sequence = full_seq[start:end]

        # rev comp if reverse strand
        if strand == '-':
            sequence = list(sequence)[::-1]
            for i, c in enumerate(sequence):
                sequence[i] = comp[c]
            sequence = ''.join(sequence)

        # check while running
        print(sequence)

        # write formatted file
        with open('e_coli_2.out', 'a') as fasta:
            fasta.write(geneid + '\t')
            for counter, character in enumerate(sequence):
                fasta.write(character)
            fasta.write('\n')


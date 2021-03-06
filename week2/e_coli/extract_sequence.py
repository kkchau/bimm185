import os

# complement dictionary
comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}

# store full sequence
full_seq = ''
with open('GCF_000005845.2_ASM584v2_genomic.fna', 'r') as sequence_file:
    next(sequence_file)
    for line in sequence_file:
        full_seq += line.strip()

fasta = {}      # id: sequence

with open('ProteinTable167_161521.txt', 'r') as proteins:
    next(proteins)      # skip header

    for line in proteins:
        
        # get protein information and corresponding sequence
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

        print(sequence)     # check output

        # write fasta file
        with open('e_coli.faa', 'a') as fasta:
            fasta.write('>')
            fasta.write('|'.join([replicon, locus, geneid]))
            for counter, character in enumerate(sequence):
                if counter % 70 == 0:
                    fasta.write('\n')
                fasta.write(character)
            fasta.write('\n')


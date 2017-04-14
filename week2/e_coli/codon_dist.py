import itertools
import re
from collections import defaultdict

# generate cartesian product of codons
all_codons = [''.join(c) for c in list(itertools.product('ATCG', repeat=3))]

# put stop codons at end
all_codons.remove('TAA')
all_codons.remove('TAG')
all_codons.remove('TGA')
all_codons.extend(['TAA', 'TAG', 'TGA'])

# dictionary to count totals
all_counts = defaultdict(int)

# total length
total = 0

# open file
with open('e_coli_2.out', 'r') as seq:
    with open('eColi_codon_table.out', 'w') as table:
        table.write('Gene\t')
        table.write('\t'.join(all_codons) + '\tLength\n')

        for line in seq:
            codon_count = defaultdict(int)          # map codons to their counts
            line = line.strip().split()

            # check if proper sequence
            if len(line[1]) % 3:
                continue

            table.write(line[0] + '\t')                 # write id

            this_codons = re.findall('...', line[1])    # break sequence

            # count and write codons
            for c in all_codons:
                table.write(str(this_codons.count(c)) + '\t')
                all_counts[c] += this_codons.count(c)

            table.write(str(len(this_codons)) + '\n')   # write len in codons
            total += len(this_codons)

        table.write('\t'.join(['Totals\t',
                               '\t'.join([str(all_counts[cod]) 
                                          for cod in all_codons]),
                                '\t', str(total)]))

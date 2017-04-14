from __future__ import division

with open('eColi_codon_table_formatted.out', 'r') as codon_table:
    with open('e_coli_cui.out', 'w') as cui:

        cui.write('Gene\tCUI\n')

        # get appropriate information from header and totals
        header = next(codon_table).strip().split()
        codons = header[1:-1]
        totals = next(codon_table).strip().split()[1:]
        gen_total = int(totals[-1])
        totals = totals[:-1]

        # dict to store total frequencies
        tot_freq = {}
        for t, codon in enumerate(codons):
            tot_freq[codon] = int(totals[t]) / gen_total

        # for each next line (last line is totals again)
        for line in codon_table: 
            line = line.strip().split()
            if line[0] == 'Totals':
                continue

            # store relevant information
            gen_id = line[0]
            counts = line[1:-1]
            this_total = int(line[-1])

            # check for proper sum
            total_q = 0

            # calculate CUI
            cod_ind = 0
            for index, c in enumerate(counts):
                this_codon = codons[index]
                c = int(c)

                # actual gene CUI
                cod_ind += (c / this_total) * (tot_freq[this_codon])
                total_q += (c / this_total)

            print(total_q)

            # output
            cui.write(gen_id + '\t' + str(cod_ind) + '\n')

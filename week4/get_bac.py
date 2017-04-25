import subprocess
import random


# open README with all UNIPROT numbers
with open('README', 'r') as read:

    # skip to UNIPROT entries
    for line in read:
        if 'Proteome_ID' in line:
            break

    # store all UNIPROT entries (just numbers)
    all_uniprot = []
    while len(line) > 1:
        all_uniprot.append(line.strip().split()[0])
        line = next(read)

# randomly select three and download
species = random.sample(all_uniprot, 3)

for s in species:
    subprocess.call(['wget', '-P', s, 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/{}_*'.format(s)])


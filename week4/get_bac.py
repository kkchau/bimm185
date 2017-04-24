import subprocess
import random


with open('README', 'r') as read:

    for line in read:
        if 'Proteome_ID' in line:
            break

    all_uniprot = []
    while len(line) > 1:
        all_uniprot.append(line.strip().split()[0])
        line = next(read)

species = random.sample(all_uniprot, 3)

for s in species:
    subprocess.call(['wget', '-P', s, 'ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Bacteria/{}_*'.format(s)])


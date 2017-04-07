from collections import defaultdict

with open('RS.txt', 'r') as input_file:
    counter = 0
    protein_interactions = defaultdict(list)
    unique_proteins = []
    for line in input_file:
        line = line.strip().split()
        if line[0] not in unique_proteins:
            counter += 1
            if counter > 2000:
                break
            unique_proteins.append(line[0])
        protein_interactions[line[0]].append([line[1], float(line[3])])

for p in unique_proteins:
    connections = protein_interactions[p]
    sort_con = sorted(connections, key=lambda x: x[1])
    print('\t'.join([p] + [str(x) for x in sort_con[len(sort_con) - 1]]))

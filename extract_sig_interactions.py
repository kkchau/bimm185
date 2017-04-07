from collections import defaultdict

with open('RS.txt', 'r') as input_file:
    protein_interactions = defaultdict(list)
    for line in input_file:
        line = line.strip().split()
        protein_interactions[line[0]].append([line[1], float(line[3])])
        if len(protein_interactions) > 2000:
            del protein_interactions[line[0]]
            break

for p in protein_interactions:
    connections = sorted(protein_interactions[p], key=lambda x: x[1])
    print('\t'.join([p] + [str(x) for x in connections[len(connections) - 1]]))

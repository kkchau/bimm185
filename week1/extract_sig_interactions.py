from collections import defaultdict

with open('RS.txt', 'r') as input_file:
    protein_interactions = defaultdict(list)
    for line in input_file:
        line = line.strip().split()
        protein_interactions[line[0]].append([line[1], float(line[3])])
        if len(protein_interactions) > 2000:
            del protein_interactions[line[0]]
            break

highest_interacting = 0
p_source = ''
p_target = ''
for p in protein_interactions:
    connections = sorted(protein_interactions[p], key=lambda x: x[1])
    if len(connections) - 1 > highest_interacting:
        highest_interacting = len(connections)
        p_source = p
        p_target = connections[len(connections) - 1][0]
    print('\t'.join([p] + [str(x) for x in connections[len(connections) - 1]]))

print(p_source, p_target, highest_interacting)

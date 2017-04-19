from __future__ import division
import sys


with open(sys.argv[1], 'r') as gen:
    g = ''.join([line.strip() for line in gen.readlines() if line[0] != '>'])
    print((g.count('G') + g.count('C')) / len(g))

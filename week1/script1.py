import re
import sys

# command line argument for input file (TCDB.faa)
filename = sys.argv[1]

# read file
with open(filename, 'r') as inputfile:

    # output file
    with open("script1.out", 'w') as out:
        
        for i, line in enumerate(inputfile):

            # remove newlines
            line = line.strip()
            
            # check for header
            if line[0] == '>':
                if i != 0:
                    out.write('\n')
                match = re.match("^>\w+\|\S+\|(.+?)\|(\S+)", line)
                out.write(match.group(2) + '-' + match.group(1) + '\t')
            else:
                out.write(line)

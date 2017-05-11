"""
    Populate the operons table based on information found 
        in ./SampleFiles/OperonSet.txt                                         
"""


import pymysql
import subprocess


# all operons that are strong or confirmed
operons_lines = subprocess.check_output(['grep', '\"^[^#]\"]', 
                                         './SampleFiles/OperonSet.txt']
                                       ).splitlines()

confirmed_operons = {}      # map genes to their operons
for line in operons_lines:
    line = line.strip().split()
    if 'Strong' in line[len(line) - 1] or 'Confirmed' in line[len(line) - 1]:
        genes = line[5].strip().split(',')
        for g in genes:
            

import subprocess
import getpass
import pymysql


sqlcon = pymysql.connect(host='bm185s-mysql.ucsd.edu',
                         user='kkchau',
                         db='kkchau_db',
                         passwd=getpass.getpass("Input password: ")
                        )

cur = sqlcon.cursor()


# map locus tag to gene name from GeneProductSet.txt
gp_set = subprocess.check_output(
    ["grep", "^[^#]", "../week6/SampleFiles/GeneProductSet.txt"]
).splitlines()
gp_set = [line.decode('ascii').strip().split() for line in gp_set]

locus_map = {
    entry[1]: entry[2] for entry in gp_set if len(entry) > 2
}


# get operon membership
op_set = subprocess.check_output(
    ["grep", "^[^#]", "../week6/SampleFiles/OperonSet.txt"]
).splitlines()
op_set = [line.decode('ascii').strip().split() for line in op_set]

# calculate intergenic distances between genes of the same operon
for operon in op_set:

    # is there information for every gene in this operon?
    operon_complete = True

    # array to hold gene information
    gene_info_set = []

    # only strong or confirmed operons
    if 'Strong' not in operon[-1] and 'Confirmed' not in operon[-1]:
        continue

    # convert genes to b_nums
    b_num = [locus_map[gene_member] 
             for gene_member in operon[5].strip().split(',')
            ]

    # get left coordinate, right coordinate, and strand for each locus_tag
    for b in b_num:

        left = None
        right = None
        gene_id = None
        strand = None
        
        # get left coordinate
        cur.execute("SELECT l_position FROM exons e JOIN genes g USING(gene_id)"
                    + " WHERE g.locus_tag='{}'".format(b)
                    + " ORDER BY l_position ASC LIMIT 1;"
                   )

        l_result = cur.fetchone()

        if l_result:    
            left = l_result[0]

        # right coordinate
        cur.execute("SELECT r_position FROM exons e JOIN genes g USING(gene_id)"
                    + " WHERE g.locus_tag='{}'".format(b)
                    + " ORDER BY r_position DESC LIMIT 1;"
                   )

        r_result = cur.fetchone()

        if r_result:
            right = r_result[0]

        # strand
        cur.execute(
            "SELECT gene_id, strand FROM genes WHERE locus_tag='{}'".format(b)
        )

        s_result = cur.fetchone()

        if s_result:
            gene_id = s_result[0]
            strand = s_result[1]

        # if there is insufficient information for this gene
        # skip the entire operon
        # if not left or not right or not strand:
        #     operon_complete = False

        # else:
        #     gene_info_set.append((gene_id, left, right, strand))
        if not left or not right or not strand:
            continue
        else: 
            gene_info_set.append((gene_id, left, right, strand))

    for gene in gene_info_set:
        print(operon[0], gene)
        cur.execute(
            "INSERT INTO operons VALUES (%s,%s,%s,%s,%s,%s);",
            (gene[0],operon[0],operon[-1],gene[1],gene[2],gene[3])
        )
        sqlcon.commit()

sqlcon.close()


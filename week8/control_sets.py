import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde
import pymysql
import getpass
import math


def pos_control(sqlcon):
    """
        Calculate the positive control values
        Values are intergenic distances within the same operon
        Returns an array with all distances
    """

    distances = []

    cur = sqlcon.cursor()

    # get the ordered set of disjoint operons
    cur.execute(
        "SELECT DISTINCT operon FROM operons ORDER BY l_pos;")
    operons = [op[0] for op in cur.fetchall()]

    # calculate distances for each operon
    for op in operons:

        # all coordinates into arrays
        cur.execute(
            "SELECT l_pos,r_pos,gene_id FROM operons WHERE operon='{}'".format(op)
            + " ORDER BY l_pos;"
        )
        coordinates = cur.fetchall()

        # ignore single-gene operons
        if len(coordinates) < 1:
            continue

        lp_array = [coord[0] for coord in coordinates]      # left_pos
        rp_array = [coord[1] for coord in coordinates]      # right_pos
        gid_array = [coord[2] for coord in coordinates]     # gene_ids

        # distances
        for ind in range(len(rp_array) - 1):
            distance = lp_array[ind + 1] - rp_array[ind] + 1
            """
            if distance > 200:
                print(gid_array[ind], gid_array[ind+1], distance)
                continue
            """
            distances.append(
                lp_array[ind + 1] - rp_array[ind] + 1
            )

    return distances


def neg_control(sqlcon):
    """
       Calculate negative control values
       Values are distances between operons on the same strand
       Returns an array with all distances
    """
    distances = []

    cur = sqlcon.cursor()

    # get the ordered set of disjoint operons
    cur.execute(
        "SELECT DISTINCT operon FROM operons ORDER BY l_pos;")
    operons = [[op[0]] for op in cur.fetchall()]

    # get left-most gene and right-most gene and strand for each operon
    for i, operon in enumerate(operons):
        cur.execute("SELECT gene_id FROM operons"
                    + " WHERE operon='{}' ORDER BY l_pos limit 1;".format(operon[0]))
        
        operons[i].append(cur.fetchone()[0])

        cur.execute("SELECT gene_id,strand FROM operons"
                    + " WHERE operon='{}' ORDER BY r_pos DESC limit 1;".format(operon[0]))

        operons[i].extend(list(cur.fetchone()))

    # get distances between genes of disjoint operons
    for operon in operons:
        left_gene = operon[1]
        right_gene = operon[2]
        strand = operon[3]
        b_strand = None
        a_strand = None

        # operon's left gene
        cur.execute("SELECT l_position FROM exons WHERE gene_id='{}' LIMIT 1;".format(left_gene))
        result = cur.fetchone()
        if result:
            left_left = result[0]

        # operon's right gene
        cur.execute("SELECT r_position FROM exons WHERE gene_id='{}' LIMIT 1;".format(right_gene))
        result = cur.fetchone()
        if result:
            right_right = result[0]

        # gene before left gene
        cur.execute("SELECT r_position,strand FROM exons JOIN genes USING (gene_id) WHERE r_position < {} and genome_id=1 ORDER BY r_position DESC LIMIT 1;".format(left_left))
        result = cur.fetchone()
        if result:
            before_left,b_strand = result

        # gene after right gene
        cur.execute("SELECT l_position,strand FROM exons JOIN genes USING (gene_id) WHERE l_position > {} and genome_id=1 ORDER BY l_position ASC LIMIT 1;".format(right_right))
        result = cur.fetchone()
        if result:
            after_right,a_strand = result

        if b_strand == strand:
            distances.append(int(left_left) - int(before_left))

        if a_strand == strand:
            distances.append(int(after_right) - int(right_right))

    return distances


def main():
    """
        Main function
    """

    sql_connection = pymysql.connect(
        host='bm185s-mysql.ucsd.edu',
        user='kkchau',
        db='kkchau_db',
        passwd=getpass.getpass("Input password: ")
    )

    pctr = pos_control(sql_connection)
    nctr = neg_control(sql_connection)

    # create seaborn plots and save image
    density_pos = gaussian_kde(pctr)
    density_neg = gaussian_kde(nctr)
    x_samples = np.arange(-20, 200, 0.5)
    plt.xlim(-20, 200)
    plt.plot(x_samples, density_pos(x_samples))
    plt.plot(x_samples, density_neg(x_samples))
    plt.savefig('ctr_graph_8.png')
    

if __name__ == '__main__':
    main() 

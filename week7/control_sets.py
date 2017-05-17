import pymysql
import getpass


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
            "SELECT l_pos, r_pos FROM operons WHERE operon='{}'".format(op)
            + " ORDER BY l_pos;"
        )
        coordinates = cur.fetchall()

        # ignore single-gene operons
        if len(coordinates) < 1:
            continue

        lp_array = [coord[0] for coord in coordinates]      # left_pos
        rp_array = [coord[1] for coord in coordinates]      # right_pos

        print(lp_array)
        print(rp_array)

        # distances
        for ind in range(len(rp_array) - 1):
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

    # get l_pos and strand
    for i, operon in enumerate(operons):
        cur.execute(
            "SELECT l_pos,strand FROM operons"
            + " WHERE operon='{}'".format(operon[0])
            + " ORDER BY l_pos LIMIT 1;"
        )

        # add l_pos, strand to operon in memory
        operons[i].extend(list(cur.fetchone()))

    # get right coordinate for each operon
    for i, operon in enumerate(operons):
        cur.execute(
            "SELECT r_pos FROM operons WHERE operon='{}'".format(operon[0])
            + " ORDER BY r_pos DESC LIMIT 1;"
        )

        # add r_pos to the operon in memory
        operons[i].insert(2, cur.fetchone()[0])

    # calculate distances between operons
    for op_ind in range(len(operons) - 1):

        # skip if not in the same strand
        if operons[op_ind + 1][3] != operons[op_ind][3]:
            continue

        distances.append(
            operons[op_ind + 1][1] - operons[op_ind][2] + 1
        )

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
    print(pctr)

    nctr = neg_control(sql_connection)
    print(nctr)


if __name__ == '__main__':
    main() 

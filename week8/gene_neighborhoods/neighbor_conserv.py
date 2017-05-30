import pymysql
import getpass


def neighbors(gene_id, cur):
    """
        Get all the neighbors of the given gene_id within the same replicon
        Returns: set of gene_ids within +/-5 genes from the given gene_id
    """
    gid_set = []
    # get the replicon id
    cur.execute(
        "SELECT replicon_id FROM genes WHERE gene_id={}".format(gene_id)
    )
    rep_id = cur.fetchone()[0]
    # get all neighbors
    for i in range(-5, 6):
        # skip self
        if i == 0:
            continue
        # get neighbor if exists in same replicon
        cur.execute(
            "SELECT gene_id FROM genes WHERE gene_id={}".format(i + gene_id)
            + " AND replicon_id={} ORDER BY start ASC;".format(rep_id)
        )
        result = cur.fetchone()
        # if a neighbor has been found
        if result:
            gid_set.append(result[0])
    return gid_set


def get_orthologs(gene_id, cur):
    """
        Returns all orthologs, as a list, for the given gene_id
    """
    ortho_set = []

    # get protein id
    cur.execute(
        "SELECT protein_id FROM genes WHERE gene_id={}".format(gene_id)
    )
    prot_id = cur.fetchone()[0]

    # get ortholog
    cur.execute(
        "SELECT seqid_2 FROM homology_1 WHERE seqid_1='{}'".format(prot_id)
    )
    result = [r1[0] for r1 in cur.fetchall()]

    # convert protein id to gene id
    for r in result:
        cur.execute(
            "SELECT gene_id FROM genes WHERE protein_id='{}'".format(r)
        )
        ortho_set.append(cur.fetchone()[0])

    # repeat
    cur.execute(
        "SELECT seqid_1 FROM homology_1 WHERE seqid_1='{}'".format(prot_id)
    )
    result = [r2[0] for r2 in cur.fetchall()]
    for r in result:
        cur.execute(
            "SELECT gene_id FROM genes WHERE protein_id='{}'".format(r)
        )
        ortho_set.append(cur.fetchone()[0])

    # return distinct set
    return list(set(ortho_set))


def conservation(cur):
    """
        Get conserved gene neighborhoods
        Returns the intersection of a gene's neighborhood
            and its orthologs' neighborhoods
    """
    # get all e_coli genes
    cur.execute(
        "SELECT DISTINCT gene_id FROM genes WHERE genome_id=1;"
    )
    e_coli_genes = [res[0] for res in cur.fetchall()]

    # for each gid
    for gene in e_coli_genes:
        conserved_neighbors = []

        # map neighbors to their orthologs
        neighbor_map = {n: get_orthologs(n, cur) for n in neighbors(gene, cur)}

        # orthologs of this gene
        orthologs = get_orthologs(gene, cur)

        for ortho in orthologs:
            for o_n in neighbors(ortho, cur):
                for g_n in neighbor_map:

                    # if the ortholog neighbors are in the set of neighbors
                    if o_n in neighbor_map[g_n]:
                        conserved_neighbors.append((g_n, o_n - ortho))
                        break

        # write to flat file
        with open('output.txt', 'a') as output:
            for c_n in conserved_neighbors:
                output.write('\t'.join(
                    [str(gene), str(c_n[0]), str(abs(gene - c_n[0])), str(abs(c_n[1]))]
                ))
                output.write('\n')
    return 0


def main():
    """
        Main function
    """
    connection = pymysql.connect(
        host='bm185s-mysql.ucsd.edu',
        user='kkchau',
        db='kkchau_db',
        passwd=getpass.getpass("Input password: ")
    )

    cursor = connection.cursor()

    conservation(cursor)


if __name__ == '__main__':
    main()

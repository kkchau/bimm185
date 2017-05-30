"""
    Calculate orthologous sequences using Ortholog-Higher-Than-Paralog method
"""


import pymysql
import getpass


def top_score_self(cur, qseqid, gen):
    """
        Find the top-scoring hit for the given query within its own genome
        Takes as parameters cursor, query_id, genome number
    """
    cur.execute(
        "SELECT sseqid,bitscore FROM blast_gid{}_self".format(gen)
        + " WHERE qseqid='{}' ORDER BY bitscore DESC LIMIT 1;".format(qseqid)
    )
    return cur.fetchone()


def ohtp(cur, gen):
    """
        Find all sseqids from comparison genome where their bitscore is higher
        than the paralog bitscore
    """
    # set of distinct qseqid
    cur.execute(
        "SELECT DISTINCT qseqid FROM blast_gid{}_self;".format(gen)
    )
    seq_top_score = {
        res[0]: top_score_self(cur, res[0], gen) for res in cur.fetchall()
    }

    # get ortholog with higher bitscore for each qseqid
    for qseqid in seq_top_score:
        print(seq_top_score[qseqid][1])
        cur.execute(
            "SELECT sseqid FROM blast_gid{}".format(gen)
            + " WHERE bitscore>{}".format(seq_top_score[qseqid][1])
            + " AND qseqid='{}';".format(qseqid)
        )
        result = [r[0].strip().split('|')[1] for r in cur.fetchall()]
        print(result)
        for hit in result:
            cur.execute(
                "INSERT INTO homology_1 VALUES ('{}','{}','{}','{}');".format(
                    qseqid, hit, 'Orthology', 'OHTP')
            )
    return cur


def main():
    """
        Main function
    """
    connection = pymysql.connect(
        host='bm185s-mysql.ucsd.edu',
        user='kkchau',
        passwd=getpass.getpass("Input password: "),
        db='kkchau_db'
    )
    cursor = connection.cursor()

    cursor = ohtp(cursor, 1)
    connection.commit()
    cursor = ohtp(cursor, 2)
    connection.commit()


if __name__ == '__main__':
    main()

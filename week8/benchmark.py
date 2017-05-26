"""
    Benchmarking our operon Bayesian inference model
    Calculation of probability of common operon membership per gene-pair
    Uploads to SQL database: table_name=tus
"""

import pymysql
import getpass
import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from control_sets import pos_control
from control_sets import neg_control
from inference_model import posterior_prob


def bench(connection, threshold):
    """
        Uploads prediction of operon memberships to database
        Fields: gene_id, gene_id, distance, status, probability
        Table Name: tus
    """

    cur = connection.cursor()

    # get all genes in increasing order of position, along with strand
    cur.execute(
        "SELECT gene_id,start,end,strand FROM genes"
        + " WHERE genome_id=1 ORDER BY start;"
    )
    result = cur.fetchall()

    gene_array = [tuple(g) for g in result]

    # posterior function
    posterior = posterior_prob(
        gaussian_kde(pos_control(connection)), 
        gaussian_kde(neg_control(connection))
    )

    # iterate through gene array and get distances
    for index, gene in enumerate(gene_array[:-1]):
        
        next_gene = gene_array[index + 1]

        # skip if different strands
        if gene[3] != next_gene[3]:
            continue

        dist = int(next_gene[1]) - int(gene[2])
        prob = posterior(dist)[0]
        status = None

        # check if same operon or different operon
        cur.execute(
            "SELECT operon FROM operons"
            + " WHERE gene_id={}".format(gene[0])
        )
        fetch = cur.fetchone()
        this_operon = fetch[0] if fetch else ''
        cur.execute(
            "SELECT operon FROM operons"
            + " WHERE gene_id={}".format(next_gene[0])
        )
        fetch = cur.fetchone()
        next_operon = fetch[0] if fetch else ''

        # status cases
        # TP: True Positive; TN: True Negative;
        # FP: False Positive; FN: False Negative;
        # PD: Prediction
        if this_operon == next_operon and this_operon != '' and next_operon != '':
            if prob > threshold:
                status = '\"TP\"'
            else:
                status = '\"FN\"'
        elif this_operon != next_operon and this_operon != '' and next_operon != '':
            if prob < threshold:
                status = '\"TN\"'
            else:
                status = '\"FP\"'
        else:
            status = '\"PD\"'

        fields = [
            gene[0], next_gene[0], dist, status, prob
        ]
        fields = ','.join([str(value) for value in fields])
        cur.execute(
            "INSERT INTO tus VALUES"
            + " ({});".format(fields)
        )

        connection.commit()


def pred_power(connection):
    """
        Determine the predictive power of each threshold for table: tus
        Returns a list of dictionaries for values of:
            True positives, True negatives, False positives, False negatives
    """
    thresh_set = np.arange(0, 1, 0.05)
    counts = []
    for threshold in thresh_set:
        cur = connection.cursor()
        cur.execute("TRUNCATE tus;")
        connection.commit()

        bench(connection, threshold)

        # get values for TP, TN, FP, FN
        bench_vals = {'tp': 0, 'tn': 0, 'fp': 0, 'fn': 0}
        for val in bench_vals:
            cur.execute("SELECT COUNT(*) FROM tus WHERE status='{}'".format(val))
            result = cur.fetchone() 
            if result:
                bench_vals[val] = result[0]
        counts.append(bench_vals)

    return counts


def svs(bench_vals):
    """
        Create Specificity and Sensitivity arrays from a benchmark array
        Uses table tus
        Returns arrays for specificity and sensitivity
    """
    sens = []
    spec = []
        
    for vals in bench_vals:
        if vals['tp'] > 0 or vals['fp'] > 0:
            sens.append(
                vals['tp'] / (vals['tp'] + vals['fn'])
            )
        else:
            sens.append(0)
        if vals['tn'] > 0 or vals['fn'] > 0:
            spec.append(
                vals['tn'] / (vals['tn'] + vals['fp'])
            )
        else:
            spec.append(0)

    return sens, spec


def roc(bench_vals):
    """
        Create receiver operator curve values from an array of benchmark values
        Uses table: tus
        Returns two arrays: True Positive Rate and False Positive Rate
    """
    tpr = []
    fpr = []
    for value in bench_vals:
        if value['tp'] + value['fn'] != 0:
            tpr.append(value['tp'] / (value['tp'] + value['fn']))
        else:
            tpr.append(0)
        if value['tn'] + value['fp'] != 0:
            fpr.append(value['fp'] / (value['tn'] + value['fp']))
        else:
            fpr.append(0)

    return tpr, fpr


def acc(bench_vals):
    """
        Return an array of accuracy values for each set of benchmark values
    """
    return [
        (val['tp'] + val['tn']) / sum(val.values()) for val in bench_vals
    ]


def ppv(bench_vals):
    """
        Return an array of positive predicitive values for each
            set of benchmark values
    """
    return [
        val['tp'] / (val['tp'] + val['fp']) for val in bench_vals
    ]


def main():
    """
        Main function to hide global variables
    """
    # connection
    con = pymysql.connect(
        host='bm185s-mysql.ucsd.edu',
        user='kkchau',
        db='kkchau_db',
        passwd=getpass.getpass("Input password: ")
    )

    print("Benchmarking")
    benchmarking_values = pred_power(con)
    print("SVS")
    sensitivity, specificity = svs(benchmarking_values)
    print("ROC")
    true_pos, false_pos = roc(benchmarking_values)
    print("ACC")
    accuracy = acc(benchmarking_values)

    thresh_array = np.arange(0, 1, 0.05)
    svs_fig = plt.figure()
    svs_fig.suptitle("Sensitivity vs Specificity")
    ax = svs_fig.add_subplot(111)
    ax.set_xlabel("Posterior Threshold")
    ax.set_ylabel("Performance")
    ax.plot(thresh_array, sensitivity)
    ax.plot(thresh_array, specificity)
    ax.legend(['Sensitivity', 'Specificity'])
    svs_fig.savefig("svs.png")

    roc_fig = plt.figure()
    roc_fig.suptitle("Receiver Operator Curve")
    ax = roc_fig.add_subplot(111)
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.plot(false_pos, true_pos)
    roc_fig.savefig("roc.png")

    acc_fig = plt.figure()
    acc_fig.suptitle("Accuracy per Threshold Value")
    ax = acc_fig.add_subplot(111)
    ax.set_xlabel("Posterior Threshold")
    ax.set_ylabel("Accuracy")
    ax.plot(thresh_array, accuracy)
    acc_fig.savefig("acc.png")

    con.close()
    

if __name__ == '__main__':
    main()

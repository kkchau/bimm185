"""
    Creation of inference models
"""


import numpy as np
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import pymysql
import getpass
import math
import os
from contextlib import redirect_stdout

from control_sets import pos_control
from control_sets import neg_control


def posterior_prob(kdep, kden):
    """
        Creates a posterior-probability function
            based on the given positive and negative control
            gaussian kernal density estimate functions
        Priors are given as h_1=0.6 and h_0=0.4
    """

    def _probability(x):
        return ((kdep(x)*0.6) / ((kdep(x)*0.6) + (kden(x)*0.4)))

    return _probability


def main():
    
    sqlcon = pymysql.connect(
        host='bm185s-mysql.ucsd.edu',
        user='kkchau',
        db='kkchau_db',
        passwd=getpass.getpass("Input password: ")
    )

    p_kde = gaussian_kde(pos_control(sqlcon))
    n_kde = gaussian_kde(neg_control(sqlcon))
    post = posterior_prob(p_kde, n_kde)
    
    """
    # graphing
    x_samples = np.arange(-40, 300, 0.5)
    plt.plot(x_samples, post(x_samples))
    plt.plot(x_samples, p_kde(x_samples))
    plt.plot(x_samples, n_kde(x_samples))
    plt.legend(['Posterior', 'Positive', 'Negative'])
    plt.savefig('overlap.png')
    plt.clf()
    plt.plot(x_samples, p_kde(x_samples))
    plt.title("Positive Control")
    plt.savefig("pctr.png")
    plt.clf()
    plt.plot(x_samples, n_kde(x_samples))
    plt.title("Negative Control")
    plt.savefig("nctr.png")
    """


if __name__ == '__main__':
    main()

__author__ = 'iankuoli'

import networkx as nx
import scipy.sparse as sp
import numpy as np
import operator

# (TKDE, 2007)
# Random-Walk Computation of Similarities between Nodes of a Graph with Application to Collaborative Recommendation
def rw_sim(u, v, symA, nodelist):

    nodes_num = len(nodelist)

    i = nodelist.index(u)
    j = nodelist.index(v)

    e_i = np.zeros(nodes_num)
    e_i[i] = 1
    e_j = np.zeros(nodes_num)
    e_j[j] = 1

    l_i = np.zeros(nodes_num)
    l_i[i] = 1
    l_j = np.zeros(nodes_num)
    l_j[j] = 1

    for k in range(30):
        l_i = 0.5 * symA * l_i + 0.5 * e_i
        l_j = 0.5 * symA * l_j + 0.5 * e_j

    # i -> j
    l_ii = l_i[i]
    l_ij = l_i[j]

    # j -> i
    l_ji = l_j[i]
    l_jj = l_j[j]

    ret = l_ii + l_jj - l_ij - l_ji

    return ret

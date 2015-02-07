__author__ = 'iankuoli'

import networkx as nx
import scipy.sparse as sp
import numpy as np
import operator

ComToCloseThreshold = 1

# avgMinDist: 1.1435102134  - dupboss
# avgMinDist: 1.23111763964 - comivst
avgMinDist = 0
tendersNum = 0

def row_normalize(cc):
    v = cc.sum(axis=1).T
    for k in range(v.size):
        if v[0, k] == 0:
            v[0, k] = 1e-20

    ccd = sp.spdiags(1. / v, 0, *cc.shape)
    return ccd * cc

def sym_normalize(cc):
    v = np.power(cc.sum(axis=1).T, 0.5)
    for k in range(v.size):
        if v[0, k] == 0:
            v[0, k] = 1e-20

    ccd = sp.spdiags(1. / v, 0, *cc.shape)
    return ccd * cc * ccd

G = nx.Graph()

f_graph = open('Graph_comivst', 'r')


for line in f_graph:
    l = line.strip('\n').split('\t')
    com1 = l[0]
    com2 = l[1]
    w = float(l[2])
    G.add_edge(com1, com2, dupbossjaccard=w)

'''
f_graph = open('Graph_addr', 'r')

for line in f_graph:
    l = line.strip('\n').split('\t')
    if l[2] == 'NA':
        continue
    com1 = l[0]
    com2 = l[1]
    w = (float(l[2]) + 1) / 2
    G.add_edge(com1, com2, dupbossjaccard=w)
'''
'''
f_graph = open('Graph_dupboss.csv', 'r')

for line in f_graph:
    l = line.strip('\n').split(',')
    com1 = l[0]
    com2 = l[1]
    w = float(l[2])
    G.add_edge(com1, com2, dupbossjaccard=w)
'''

nodelist = G.nodes()
nodesNum = len(nodelist)
edgesNum = len(G.edges())
A = nx.to_scipy_sparse_matrix(G, nodelist=nodelist, weight='dupbossjaccard', dtype=float)
symA = sym_normalize(A)

f_tender = open('TenderTransaction_win.txt', 'r')

dictTenders = dict()

for line in f_tender:
    l = line.strip('\n').split('\t')
    tenderID = l[0]
    tenders = set(l[1].split(','))
    winner = l[2]

    '''
    if tenderID == '50893171':
        print(50893171)
    '''

    if winner not in nodelist or len(tenders) == 1 or winner == '-1':
        continue

    dictDistance = dict()

    dictDistance[winner] = 0

    minSim = 100000

    for d in tenders:

        if d not in nodelist or winner == d:
            continue

        i = nodelist.index(winner)
        j = nodelist.index(d)

        e_i = np.zeros(nodesNum)
        e_i[i] = 1
        e_j = np.zeros(nodesNum)
        e_j[j] = 1

        l_i = np.zeros(nodesNum)
        l_i[i] = 1
        l_j = np.zeros(nodesNum)
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

        dictDistance[d] = l_ii + l_jj - l_ij - l_ji

        '''
        if l_ii + l_jj < l_ij + l_ji:
            print(str(l_ii) + ', ' + str(l_jj) + ', ' + str(l_ij) + ', ' + str(l_ji))
        '''

        if 0 < dictDistance[d] < minSim:
            minSim = dictDistance[d]

    if minSim < 100000:
        avgMinDist += minSim
        tendersNum += 1

    if minSim < ComToCloseThreshold:
        dictTenders[tenderID] = dictDistance
        print(tenderID)


f_BidRigging = open('BidRiggingSuspicion_comivst_' + str(ComToCloseThreshold) + '.txt', 'w')

for tenderID in dictTenders.keys():
    dictDist = dictTenders[tenderID]
    sorted_Dist = sorted(dictDist.items(), key=operator.itemgetter(1))

    strWrite = tenderID

    for i in sorted_Dist:
        strWrite += '\t' + str(i[0]) + ':' + str(i[1])

    strWrite += '\n'

    f_BidRigging.write(strWrite)

if tendersNum > 0:
    print('\n avgMinDist: ' + str( avgMinDist / tendersNum))
else:
    print('\n avgMinDist: 0')

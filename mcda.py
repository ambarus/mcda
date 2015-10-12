#!/usr/bin/env python
# encoding: utf-8
"""On Multi-controller Placement Optimization implementation"""

import random

__author__ = """\n""".join(['Tudor Ambarus <tudor.ambarus@gmail.com>'])
__copyright__ = ""
__license__ = ""
__version__ = ""
__email__ = "tudor.ambarus@gmail.com"
__status__ = "Development"

from collections import defaultdict
from itertools import combinations
import networkx as nx
from algs import *
from args import *
from draw import *

def mcda_alg(G, cplacement):
    '''
    Compute shortest path lengths between all nodes in a weighted graph.
    g_path_len will be a dictionary, keyed by source and target, of shortest
    path lengths
    '''
    g_path_len=nx.all_pairs_dijkstra_path_length(G)

    '''
    Construct decision parameters dictionary of dictionaries.
    dparam will be keyed by decision parameter and Ci placement.
    '''
    dparams = defaultdict(dict)
    for ci, ci_value in cplacement.iteritems():
        if args.a:
            dparams[1][ci] = average_latency(g_path_len, ci_value)
        if args.w:
            dparams[2][ci] = worst_latency(g_path_len, ci_value)
        if args.i:
            dparams[3][ci] = inter_controller_latency(g_path_len, ci_value)

    # use static levels in order to check the correctness of algorithms
    if False:'''
    for k, v in dparams.iteritems():
        # set reservation level
        r.append(max(v.itervalues()))
        # set aspiration level
        a.append(min(v.itervalues()))
    '''
    else:
        # static reservation level
        r = [3, 6, 6]
        # static aspiration level
        a = [0, 0, 0]

    # construct list of arguments
    largs = []
    if args.a:
        largs.append(args.a)
    if args.w:
        largs.append(args.w)
    if args.i:
        largs.append(args.i)

    for k, v in dparams.iteritems():
        # lists are indexed starting with int(0) value
        t = k-1
        for i in range (1,ci+1):
            dparams[k][i] = normalize_dparam(dparams[k][i], largs[t], r[t], a[t])

    '''
    Transposed decision parameters dictionaty of dictionaries.
    t_dparams will be keyed by Ci placement and decision parameter.
    '''
    t_dparams = defaultdict(dict)
    for i, v in dparams.iteritems():
        for j in range(1,ci+1):
            t_dparams[j][i] = dparams[i][j]

    '''
    Compute for each candidate solution Ci, the minimum among
    all its normalized decision parameters / variables.
    '''
    min_list = []
    for i, v in t_dparams.iteritems():
        min_list.append(min(v.itervalues()))

    print_ci_info(min_list, cplacement, args)
    draw_graph(G)

def static_execution():
    elist = [(1,5,4),(1,6,2),(2,3,5),(2,4,2),(2,5,3),(2,6,6),(3,2,5),(3,5,5),
             (3,6,2),(4,2,2),(4,5,1),(4,6,4),(5,1,4),(5,2,3),(5,3,5),(5,4,1),
             (5,6,3),(6,1,2),(6,2,6),(6,3,2),(6,4,4),(6,5,3)]
    cplacement = {1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1},
                  2: {1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0},
                  3: {1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1},
                  4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1}}

    G = nx.Graph()
    G.add_nodes_from([1,6])
    G.add_weighted_edges_from(elist)

    mcda_alg(G, cplacement)

def random_edge_list():
    edge_list = [(i, j, random.randint(1, args.n))
                 for i in range(args.n)
                 for j in range(i+1, args.n)]
    return edge_list

def controller_pairs():
    cplacement = defaultdict(dict)
    liste = [x for x in combinations(range(args.n), args.c)]

    for i in range(len(liste)):
        for j in range(args.c):
            cplacement[i][liste[i][j]] = 1
    return cplacement

def dynamic_execution():
    edge_list = random_edge_list()

    #all controller placement combinations
    cplacement = controller_pairs()

    G = nx.Graph()
    G.add_nodes_from([0, args.n - 1])
    G.add_weighted_edges_from(edge_list)

    mcda_alg(G, cplacement)

if __name__ == '__main__':
    # parse user arguments
    args, nargs = parse_args()

    if not args.dynamic:
        static_execution()
    else:
        dynamic_execution()

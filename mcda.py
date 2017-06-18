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
            dparams[0][ci] = average_latency(g_path_len, ci_value)
        if args.w:
            dparams[1][ci] = worst_latency(g_path_len, ci_value)
        if args.i:
            dparams[2][ci] = inter_controller_latency(g_path_len, ci_value)

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

    for k in dparams:
        for i in range (0,ci+1):
            dparams[k][i] = normalize_dparam(dparams[k][i], largs[k], r[k], a[k])

    '''
    Compute for each candidate solution Ci, the minimum among
    all its normalized decision parameters / variables.
    '''
    max_cost = 999
    min_dparam = []
    for i in range (0,ci+1):
	min_dparam.append(max_cost)

    for ci_dict in dparams.itervalues():
	for ci, dparam_value in ci_dict.iteritems():
             min_dparam[ci] = min(min_dparam[ci], dparam_value)

    '''select the best ci placement, the one having the highest
       of the minimum normalized decision parameters'''
    result = min_dparam.index(max(min_dparam))

    print_ci_info(result, cplacement)
    draw_graph(G)

def static_execution():
    """
    Edge list is composed of tuples defined as:
    (node_x, node_y, weight_between_x_and_y)
    """
    elist = [(0,4,4),(0,5,2),(1,2,5),(1,3,2),(1,4,3),(1,5,6),(2,1,5),(2,4,5),
             (2,5,2),(3,1,2),(3,4,1),(3,5,4),(4,0,4),(4,1,3),(4,2,5),(4,3,1),
             (4,5,3),(5,0,2),(5,1,6),(5,2,2),(5,3,4),(5,4,3)]

    """
    Dictionary of dictionary. The parent represent the controller placement
    solutions. There are 4 proposed solutions. The childs are keyed by the
    node number and value 1 represent that the node is a controller.
    """
    cplacement = {0: {0: 0, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1},
                  1: {0: 0, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0},
                  2: {0: 0, 1: 0, 2: 1, 3: 0, 4: 0, 5: 1},
                  3: {0: 0, 1: 0, 2: 0, 3: 1, 4: 0, 5: 1}}


    """create an empty graph"""
    G = nx.Graph()
    G.add_nodes_from([0,5])
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

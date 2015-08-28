#!/usr/bin/env python
# encoding: utf-8
"""On Multi-controller Placement Optimization implementation"""

from __future__ import division
import random

__author__ = """\n""".join(['Tudor Ambarus <tudor.ambarus@gmail.com>'])
__copyright__ = ""
__license__ = ""
__version__ = ""
__email__ = "tudor.ambarus@gmail.com"
__status__ = "Development"

from collections import defaultdict
from itertools import combinations
import argparse
import networkx as nx
import matplotlib.pyplot as plt


def restricted_float(x):
    #Define a restricted float data type in interval (0, 1].
    x = float(x)
    if x <= 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("%r not in range (0.0, 1.0]"%(x,))
    return x

def parse_args():
    """Parse user arguments

    Returns
    -------
    args : Namespace object with user arguments
    nargs : Number of user arguments
    """
    parser = argparse.ArgumentParser(description=
                                     "Multi-criteria optimization algorithm")
    parser.add_argument("-a", type=restricted_float,
                        help="Average latency - failure free scenario. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("-w", type=restricted_float,
                        help="Worst case latency - failure free scenario. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("-i", type=restricted_float,
                        help="Inter controller latency. "
                        "Expects a weight (priority) in interval (0, 1]. ")
    parser.add_argument("--static", help="Use default static undirected graph",
                        action="store_true")
    parser.add_argument("-n", type=int, help="Number of graph nodes")
    parser.add_argument("-c", type=int, help="Number of controllers in graph. "
                        "Allowed values are between N/3 and N/7")
    #parser.add_argument("-c", "--controlers", dest="controlers", metavar="C",
                         #default=2, type=int, help="Number of controlers")
    args = parser.parse_args()
    if not (args.a or args.w or args.i):
        raise parser.error("No action requested, add -a or -w or -i option")
    # nr of args
    nargs = 0
    if args.a:
        nargs = nargs + 1
    if args.w:
        nargs = nargs + 1
    if args.i:
        nargs = nargs + 1

    return args, nargs

def average_latency(g_path_len, ci):
    """Average latency for a graph and a specific Ci controller placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci : particular placement of controllers. Dictionary is keyed by node and
         has value int(1) if controller identifies with keyed node.

    Returns
    ------
    Average latency for a graph and a specific Ci controller placement
    """
    avg = 0
    for source, s_value in g_path_len.iteritems():
        # list of lengths from source to Ci domain
        s_ci_len = []
        for target, t_value in s_value.iteritems():
            if target in ci:
                if ci[target]:
                    s_ci_len.append(t_value)
        avg = avg + min(s_ci_len)

    return avg / len(g_path_len)

def worst_latency(g_path_len, ci):
    """Source to controller worst case latency for a graph and a specific
    Ci controller placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci : particular placement of controllers. Dictionary is keyed by node and
         has value int(1) if controller identifies with keyed node.

    Returns
    ------
    Source to controller worst case latency for a graph and a specific
    Ci controller placement
    """
    # list of minimum lengths from sources to Ci domain
    s_ci_min_len = []
    for source, s_value in g_path_len.iteritems():
        # list of lengths from source to Ci domain
        s_ci_len = []
        for target, t_value in s_value.iteritems():
            if target in ci:
                if ci[target]:
                    s_ci_len.append(t_value)
        s_ci_min_len.append(min(s_ci_len))

    return max(s_ci_min_len)

def inter_controller_latency(g_path_len, ci):
    """Inter controller latency for a graph and a specific Ci controller
    placement

    Parameters
    ----------
    g_path_len : dictionary of dictionaries containing shortest path lengths
                 between all nodes in a weighted graph.
                 g_path_len is keyed by source and target, of shortest path
                 lengths
    ci : particular placement of controllers. Dictionary is keyed by node and
         has value int(1) if controller identifies with keyed node.

    Returns
    -------
    Inter controller latency for a graph and a specific Ci controller placement
    """
    icl_path_len = []
    for source, s_value in g_path_len.iteritems():
        if source in ci:
                if ci[source]:
                    for target, t_value in s_value.iteritems():
                        if target in ci:
                            if ci[target]:
                                icl_path_len.append(g_path_len[source][target])
                    # compute only 1:N controller-to-controllers distances
                    break

    return max(icl_path_len)

def normalize_dparam(dparam, weight, r, a):
    """Normalize decision parameter

    Parameters
    ----------
    dparam : decision parameter
    weght : weight of decision parameter
    r : reservation level
    a : aspiration level

    Returns
    -------
    Normalized decision variable.
    """
    return weight * (r - dparam) / (r - a)

def draw_graph(G, min_list):
    #temporary printing
    result = min_list.index(max(min_list)) + 1
    # make selection among solutions
    print "Optimum Ci placement is Ci =", result
    if result == 1:
        print "Controllers are placed in nodes 5 and 6"
    elif result ==2:
        print "Controllers are placed in nodes 5 and 3"
    elif result ==3:
        print "Controllers are placed in nodes 3 and 6"
    else:
        print "Controllers are placed in nodes 4 and 6"

    # positions for all nodes
    pos=nx.spring_layout(G)

    # draw graph
    nx.draw(G,pos)
    nx.draw_networkx_labels(G,pos,node_size=700)
    # nx.draw_networkx_edge_labels(G,pos)
    edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)

    # display graph
    plt.show()


def mcda_alg(G, elist, cplacement):
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

    draw_graph(G, min_list)

def static_execution(args, nargs):
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

    mcda_alg(G, elist, cplacement)

def random_edge_list(args):
    edge_list = [(i, j, random.randint(1, args.n))
                 for i in range(args.n)
                 for j in range(i+1, args.n)]
    return edge_list

def controller_pairs(args):
    cplacement = defaultdict(dict)
    liste = [x for x in combinations(range(args.n), args.c)]

    for i in range(len(liste)):
        for j in range(args.c):
            cplacement[i][liste[i][j]] = 1
    return cplacement

def dynamic_execution(args, nargs):
    edge_list = random_edge_list(args)

    #all controller placement combinations
    cplacement = controller_pairs(args)

    G = nx.Graph()
    G.add_nodes_from([0, args.n - 1])
    G.add_weighted_edges_from(edge_list)

    mcda_alg(G, edge_list, cplacement)

if __name__ == '__main__':
    # parse user arguments
    args, nargs = parse_args()

    if args.static:
        static_execution(args, nargs)
    else:
        dynamic_execution(args, nargs)

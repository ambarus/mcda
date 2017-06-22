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

def allocate_fw_to_c(G, g_path_len, ci):
    '''
    Take into consideration to assign the appartenance to controller
    in any node form G.nodes()
    '''
    fw_c = defaultdict(dict)
    for src in g_path_len.keys():
        for dst, dst_value in ci.iteritems():
            '''if dst is controller and src != dst '''
            if dst_value == 1 and src != dst:
                min_value = g_path_len[src][dst]
                controller = dst
                break
        for dst, dst_value in ci.iteritems():
            if dst_value == 1 and src != dst:
                if g_path_len[src][dst] < min_value:
                    min_value = g_path_len[src][dst]
                    controller = dst
        src_is_ctrl = False;
        for ctrl in ci.iterkeys():
            if src == ctrl:
                src_is_ctrl = True;

        if src_is_ctrl:
            fw_c[src]['min_cost_controller'] = '*'
        else:
            fw_c[src]['min_cost_controller'] = controller

    return fw_c

def backup_controller(G, g_path_len, ci, fw_c):
    for src in g_path_len.keys():
        for dst, dst_value in ci.iteritems():
            '''if dst is controller and src != dst
               and it's not the first controller'''
            if dst_value == 1 and src != dst and \
               fw_c[src]['min_cost_controller'] != dst:
                min_value = g_path_len[src][dst]
                backup_controller = dst
                break
        for dst, dst_value in ci.iteritems():
            if dst_value == 1 and src != dst and \
               fw_c[src]['min_cost_controller'] != dst:
                if g_path_len[src][dst] < min_value:
                    min_value = g_path_len[src][dst]
                    backup_controller = dst
        fw_c[src]['backup_ctrl'] = backup_controller
    return fw_c

def mcda_alg(G, cplacement):
    '''
    Compute shortest path lengths between all nodes in a weighted graph.
    g_path_len will be a dictionary, keyed by source and target, of shortest
    path lengths
    '''
    if args.gml:
        g_path_len=nx.all_pairs_dijkstra_path_length(G, weight='LinkCost')
    else:
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
        if args.gml:
            r = [3 * 22, 6 * 22, 6 *22]
        else:
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

    fw_c = defaultdict(dict)
    fw_c = allocate_fw_to_c(G, g_path_len, cplacement[result])

    if (len(cplacement[result]) > 1):
        backup_dict = defaultdict(dict)
        backup_dict = backup_controller(G, g_path_len, cplacement[result], fw_c)

    if args.gml:
        show_info(fw_c, cplacement, result)
    else:
        print_ci_info(result, cplacement)
    draw_graph(G, fw_c, args.gml)

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

def controller_pairs(n, c):
    cplacement = defaultdict(dict)
    liste = [x for x in combinations(range(n), c)]

    for i in range(len(liste)):
        for j in range(c):
            cplacement[i][liste[i][j]] = 1
    return cplacement

def random_edge_list():
    edge_list = [(i, j, random.randint(1, args.n))
                 for i in range(args.n)
                 for j in range(i+1, args.n)]
    return edge_list

def dynamic_execution():
    edge_list = random_edge_list()

    #all controller placement combinations
    cplacement = controller_pairs(args.n, args.c)

    G = nx.Graph()
    G.add_nodes_from([0, args.n - 1])
    G.add_weighted_edges_from(edge_list)

    mcda_alg(G, cplacement)

def add_int_link_cost(G):
    """
    LinkCost = 1 / Bandwith.
    LinkLabel contains Bandwith values in Mbps.
    Compute the value as 1 (Gbps) / Bandwith (Gbps)
    """
    for edge in G.edges(data=True):
        edge[2]['LinkCost'] = 1000 / int(edge[2]['LinkLabel'].split(" ")[0])

def gml_controller_pairs(G, no_c):
    '''
    cplacement will be a dictionary of dictionaries like the one
    listed above:

    {0: {u'San Diego': 1, u'Jackson': 1, u'Dallas': 1},
     1: {u'San Diego': 1, u'Jackson': 1, u'Philadelphia': 1},
     2: {u'San Diego': 1, u'Jackson': 1, u'Denver': 1},
     .
     .
     .

     2924: {u'Oakland': 1, u'New York': 1, u'Cleveland': 1}
    }
    '''
    cplacement = defaultdict(dict)
    liste = [x for x in combinations(G.node, no_c)]

    for i in range(len(liste)):
        for j in range(no_c):
            cplacement[i][liste[i][j]] = 1
    return cplacement

def run_gml():
    G=nx.read_gml('topologyzoo/sources/Bbnplanet.gml')
    add_int_link_cost(G)

    g_path_len=nx.all_pairs_dijkstra_path_length(G, weight='LinkCost')

    cplacement = gml_controller_pairs(G, 3)

    mcda_alg(G, cplacement)

if __name__ == '__main__':
    # parse user arguments
    args, nargs = parse_args()
    if args.gml:
        run_gml()
        exit()

    if not args.dynamic:
        static_execution()
    else:
        dynamic_execution()

#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
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
        if ci[source]:
            for target, t_value in s_value.iteritems():
                if ci[target]:
                    icl_path_len.append(g_path_len[source][target])
            # compute only 1:N controller-to-controllers distances
            break

    return max(icl_path_len)

if __name__ == '__main__':
    elist = [(1,5,4),(1,6,2),(2,3,5),(2,4,2),(2,5,3),(2,6,6),(3,2,5),(3,5,5),(3,6,2),(4,2,2),(4,5,1),(4,6,4),(5,1,4),(5,2,3),(5,3,5),(5,4,1),(5,6,3),(6,1,2),(6,2,6),(6,3,2),(6,4,4),(6,5,3)]
    cplacement = {1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1}, 2: {1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0}, 3: {1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1}, 4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1}}

    args=parse_args()

    G = nx.Graph()
    G.add_nodes_from([1,6])
    G.add_weighted_edges_from(elist)

    average_latency(G, cplacement)
    worst_latency(G, cplacement)
    inter_controller_latency(G, cplacement)

    # positions for all nodes
    pos=nx.spring_layout(G)

    # draw graph
    nx.draw(G,pos)
    nx.draw_networkx_labels(G,pos,node_size=700)
    # nx.draw_networkx_edge_labels(G,pos)
    edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
    # display
    #plt.show()

#!/usr/bin/env python
# encoding: utf-8

from __future__ import division
import argparse
import networkx as nx
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-criteria optimization algoritm")
    parser.add_argument("-c", "--controlers", dest="controlers", metavar="C", default=2, type=int, help="Number of controlers")
    return parser.parse_args()

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

if __name__ == '__main__':
    elist = [(1,5,4),(1,6,2),(2,3,5),(2,4,2),(2,5,3),(2,6,6),(3,2,5),(3,5,5),(3,6,2),(4,2,2),(4,5,1),(4,6,4),(5,1,4),(5,2,3),(5,3,5),(5,4,1),(5,6,3),(6,1,2),(6,2,6),(6,3,2),(6,4,4),(6,5,3)]
    cplacement = {1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1}, 2: {1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0}, 3: {1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1}, 4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1}}

    args=parse_args()

    G = nx.Graph()
    G.add_nodes_from([1,6])
    G.add_weighted_edges_from(elist)

    average_latency(G, cplacement)
    worst_latency(G, cplacement)

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

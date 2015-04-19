#!/usr/bin/env python
# encoding: utf-8

import argparse
import networkx as nx
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description="Multi-criteria optimization algoritm")
    parser.add_argument("-c", "--controlers", dest="controlers", metavar="C", default=2, type=int, help="Number of controlers")
    return parser.parse_args()

if __name__ == '__main__':
    elist = [(1,5,4),(1,6,2),(2,3,5),(2,4,2),(2,5,3),(2,6,6),(3,2,5),(3,5,5),(3,6,2),(4,2,2),(4,5,1),(4,6,4),(5,1,4),(5,2,3),(5,3,5),(5,4,1),(5,6,3),(6,1,2),(6,2,6),(6,3,2),(6,4,4),(6,5,3)]
    cplacement = {1: {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1}, 2: {1: 0, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0}, 3: {1: 0, 2: 0, 3: 1, 4: 0, 5: 0, 6: 1}, 4: {1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 1}}

    args=parse_args()

    G = nx.Graph()
    G.add_nodes_from([1,6])
    G.add_weighted_edges_from(elist)

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

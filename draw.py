#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
import matplotlib.pyplot as plt
from wrap import *

def show_info(fw_c, cplacement, result):
    print '\nOptimum controller placement is Ci =', result
    print 'Node that are controllers are marked with *'
    print '\n'
    labels = ('Node', 'Controller', 'Backup Controller')
    list_of_lists = []
    for node, prop in fw_c.iteritems():
        a_list = []
        a_list.append(node)
        a_list.append(prop['min_cost_controller'])
        a_list.append(prop['backup_ctrl'])
        list_of_lists.append(a_list)

    print indent([labels]+list_of_lists, hasHeader=True)

def print_ci_info(result, cplacement):
    print "Optimum Ci placement is Ci =", result
    for key, value in cplacement[result].iteritems():
        if value:
            print "Controller is placed in node", key

def draw_graph(G, fw_c, gml, labels=None, graph_layout='spring',
               node_size=1200, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):

    """
    these are different layouts for the network you may try
    shell seems to work best
    """
    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)

    if not gml:
        node_color = []
        for key, value in fw_c.iteritems():
            node_color.append(id(value['min_cost_controller'])%100)

    """draw graph"""
    nx.draw_networkx_nodes(G,graph_pos,node_size=node_size,
                           alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G,graph_pos,width=edge_tickness,
                           alpha=edge_alpha,edge_color=edge_color)
    """draw node labels"""
    nx.draw_networkx_labels(G, graph_pos,font_size=node_text_size,
                            font_family=text_font)
    if gml:
        edge_labels=dict([((u,v,),d['LinkCost']) for u,v,d in G.edges(data=True)])
    else:
        edge_labels=dict([((u,v,),d['weight']) for u,v,d in G.edges(data=True)])

    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels,
                                 label_pos=edge_text_pos)
    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    """show graph"""
    plt.show()


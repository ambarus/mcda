#!/usr/bin/env python
# encoding: utf-8

import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
	elist = [(1,5,4),(1,6,2),(2,3,5),(2,4,2),(2,5,3),(2,6,6),(3,2,5),(3,5,5),(3,6,2),(4,2,2),(4,5,1),(4,6,4),(5,1,4),(5,2,3),(5,3,5),(5,4,1),(5,6,3),(6,1,2),(6,2,6),(6,3,2),(6,4,4),(6,5,3)]

	G = nx.Graph()
	G.add_nodes_from([1,6])
	G.add_weighted_edges_from(elist)

	dijkstra_length=nx.all_pairs_dijkstra_path_length(G)
	print(dijkstra_length[1][6])
	print(dijkstra_length[1][1])
	print(dijkstra_length[1])

	# positions for all nodes
	pos=nx.spring_layout(G)

	# draw graph
	nx.draw(G,pos)
	nx.draw_networkx_labels(G,pos,node_size=700)
	# nx.draw_networkx_edge_labels(G,pos)
	edge_labels=dict([((u,v,),d['weight'])
	for u,v,d in G.edges(data=True)])
	nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_labels)
	# display
	plt.show()

import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
    G=nx.read_gml('topologyzoo/sources/Bbnplanet.gml')
    for edge in G.edges(data=True):
        edge[2]['LinkBandwith'] = int(edge[2]['LinkLabel'].split(" ")[0])
        print edge[2]['LinkBandwith']
    g_path_len=nx.all_pairs_dijkstra_path_length(G, weight='LinkBandwith')
    print g_path_len['Jackson']
    print dir(G)
#    for node in G.nodes(data=True):
#        print node
'''

    nx.draw(G)
    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.show()
'''

import networkx as nx
import matplotlib.pyplot as plt


if __name__ == '__main__':
    G=nx.read_graphml('topologyzoo/sources/Bbnplanet.graphml')
    print G.nodes
    print G.edges

    for node in G.nodes(data=True):
        print node
    print
    print
    for edge in G.edges(data=True):
        print edge
        print int(edge[2]['label'].split(" ")[0])

    nx.draw(G)
    plt.xlim(-0.05,1.05)
    plt.ylim(-0.05,1.05)
    plt.axis('off')
    plt.show()

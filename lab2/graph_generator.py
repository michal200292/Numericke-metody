import networkx as nx
import numpy as np


def add_edge_weights(g):
    for a, b in g.edges:
        g[a][b]['weight'] = np.round(np.random.uniform(5, 10), 2)


def find_source_and_target(g):
    for a in range(g.number_of_nodes()):
        for b in range(g.number_of_nodes() - 1, a, -1):
            if a not in g.neighbors(b):
                return a, b
    return 0, g.number_of_nodes() - 1


def generate_erdos_renyi(n, p):
    g = nx.erdos_renyi_graph(n, p)
    g = nx.convert_node_labels_to_integers(g, first_label=0)
    while not nx.is_connected(g):
        g = nx.erdos_renyi_graph(n, p)
    add_edge_weights(g)
    s, t = find_source_and_target(g)
    E = np.round(np.random.uniform(5, 10), 2)
    g.add_edge(s, t, weight=E)
    return g, s, t, E


import networkx as nx
import numpy as np


class Edge:
    def __init__(self, a, b, resistance, voltage, index):
        self.a = a
        self.b = b
        self.resistance = resistance
        self.voltage = voltage
        self.index = index
        self.current = 0


def generate_circuit(g):
    n = g.number_of_nodes()
    s = np.random.randint(0, n - 1)
    t = np.random.randint(s + 1, n)

    index = 0
    for a, b in g.edges:
        if (a, b) not in [(s, t), (t, s)]:
            resistance = max(np.round(np.random.rand(), 2), 0.01)
            g[a][b]['edge'] = Edge(a, b, resistance, 0, index)
            g[b][a]['edge'] = g[a][b]['edge']
            index += 1

    e = max(np.round(np.random.rand(), 2), 0.01)
    g.add_edge(s, t)
    g[s][t]['edge'] = Edge(s, t, 0, e, index)
    g[t][s]['edge'] = g[s][t]['edge']
    return s, t, e


def generate_erdos_renyi(n, p):
    g = nx.erdos_renyi_graph(n, p)
    while not nx.is_connected(g):
        g = nx.erdos_renyi_graph(n, p)
    g = nx.convert_node_labels_to_integers(g, first_label=0)
    s, t, e = generate_circuit(g)
    return g, s, t, e


# g, s, t, e = generate_erdos_renyi(5, 0.5)


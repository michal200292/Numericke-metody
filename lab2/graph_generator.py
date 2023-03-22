import networkx as nx
import numpy as np


class Edge:
    def __init__(self, a, b, resistance, index):
        self.a = a
        self.b = b
        self.resistance = resistance
        self.index = index
        self.current = 0


def generate_circuit(g, s=None, t=None, pos=True):
    n = g.number_of_nodes()
    if s is None:
        s = np.random.randint(0, n - 1)
        t = np.random.randint(s + 1, n)

    index = 0
    for a, b in g.edges:
        if (a, b) not in [(s, t), (t, s)]:
            resistance = max(np.round(np.random.rand(), 2), 0.01)
            g[a][b]['edge'] = Edge(a, b, resistance, index)
            g[b][a]['edge'] = g[a][b]['edge']
            index += 1

    e = max(np.round(np.random.rand(), 2), 0.01)
    g.add_edge(s, t)
    g[s][t]['edge'] = Edge(s, t, -1, index)
    g[t][s]['edge'] = g[s][t]['edge']
    if pos:
        g.graph['pos'] = nx.kamada_kawai_layout(g)
    return s, t, e


def generate_erdos_renyi(n, p, pos=True):
    if p < 0.02:
        raise AttributeError("p value to low. It might be impossible for algorithm to generate a connected graph")
    g = nx.erdos_renyi_graph(n, p)
    while not nx.is_connected(g):
        g = nx.erdos_renyi_graph(n, p)
    g = nx.convert_node_labels_to_integers(g, first_label=0)
    s, t, e = generate_circuit(g, pos=pos)
    return g, s, t, e


def generate_cubic(n, pos=True):
    if n % 2:
        raise AttributeError("n should be an even number")
    g = nx.random_regular_graph(3, n)
    g = nx.convert_node_labels_to_integers(g, first_label=0)
    s, t, e = generate_circuit(g, pos=pos)
    return g, s, t, e


def generate_bridge_graph(n, m, p1, p2, pos=True):
    if p1 < 0.02:
        raise AttributeError("p1 value to low. It might be impossible for algorithm to generate a connected graph")
    if p2 < 0.02:
        raise AttributeError("p2 value to low. It might be impossible for algorithm to generate a connected graph")
    g1 = nx.erdos_renyi_graph(n, p1)
    while not nx.is_connected(g1):
        g1 = nx.erdos_renyi_graph(n, p1)

    g2 = nx.erdos_renyi_graph(m, p2)
    while not nx.is_connected(g2):
        g2 = nx.erdos_renyi_graph(m, p2)

    g1 = nx.convert_node_labels_to_integers(g1, first_label=0)
    g2 = nx.convert_node_labels_to_integers(g2, first_label=n)
    g = nx.Graph()
    g.add_edge(np.random.randint(0, n), np.random.randint(n, n + m))
    g.add_edges_from(list(g1.edges) + list(g2.edges))
    s, t, e = generate_circuit(g, np.random.randint(0, n), np.random.randint(n, n + m), pos=pos)
    return g, s, t, e


def generate_small_world(n, k, p, pos=True):
    g = nx.connected_watts_strogatz_graph(n, k, p)
    g = nx.convert_node_labels_to_integers(g, first_label=0)
    s, t, e = generate_circuit(g, pos=pos)
    return g, s, t, e


def generate_2d_mesh(m, n, pos=True):
    g = nx.Graph()
    for i in range(m):
        for j in range(n - 1):
            g.add_edge(i*n + j, i*n + j + 1)

    for i in range(n):
        for j in range(m - 1):
            g.add_edge(j*n + i, j*n + n + i)
    s, t, e = generate_circuit(g, pos=pos)
    return g, s, t, e


def generate_triangulation(m, n, pos=True):
    g = nx.Graph()
    for i in range(m - 1):
        for j in range(n - 1):
            g.add_edge(i*n + j, i*n + j + 1)
            if np.random.randint(0, 2):
                g.add_edge(i*n + j, (i+1)*n + j + 1)
            else:
                g.add_edge((i+1)*n + j, i*n + j + 1)

    for j in range(n - 1):
        g.add_edge((m-1) * n + j, (m-1) * n + j + 1)

    for i in range(n):
        for j in range(m - 1):
            g.add_edge(j*n + i, j*n + n + i)

    s, t, e = generate_circuit(g, pos=pos)
    return g, s, t, e


def save_graph_to_file(g, s, t, E, file_name):
    with open("saved_graphs/"+file_name, 'w') as file:
        file.write(f"{s} {t} {E}\n")
        for a, b in g.edges:
            file.write(f"{a} {b} {g[a][b]['edge'].resistance}\n")


def load_graph(file_name):
    with open("saved_graphs/"+file_name, "r") as file:
        tab = file.readlines()
    vertices = [map(int, row.split()[:2]) for row in tab]
    values = [float(row.split()[-1]) for row in tab]
    g = nx.Graph()
    index = 0
    (s, t), E = vertices[0], values[0]
    for (v1, v2), R in zip(vertices[1:], values[1:]):
        if (v1, v2) != (s, t) and (v1, v2) != (t, s):
            g.add_edge(v1, v2)
            g[v1][v2]['edge'] = Edge(v1, v2, R, index)
            g[v2][v1]['edge'] = g[v1][v2]['edge']
            index += 1

    g.add_edge(s, t)
    g[s][t]['edge'] = Edge(s, t, -1, index)
    g[t][s]['edge'] = g[s][t]['edge']

    g.graph['pos'] = nx.kamada_kawai_layout(g)
    return g, s, t, E


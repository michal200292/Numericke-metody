import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import ArrowStyle


def draw_with_resistance(g, s, t, small=True):
    n = g.number_of_nodes()
    plt.figure(figsize=(10, 8))
    pos = nx.kamada_kawai_layout(g)
    labels = {}
    for i in range(n):
        labels[i] = str(i)

    if small:
        nx.draw_networkx_labels(
            g,
            pos,
            labels,
            font_size=5,
            font_color="black"
        )

    node_size = 30 if small else 10
    nx.draw_networkx_nodes(
        g,
        pos,
        nodelist=[i for i in range(n)],
        node_color="red",
        node_size=node_size,
    )

    nx.draw_networkx_nodes(
        g,
        pos,
        nodelist=[s, t],
        node_color="blue",
        node_size=30,
    )
    label_weights = {}
    for a, b in g.edges:
        label_weights[(a, b)] = str(g[a][b]['edge'].resistance)
    label_weights[(s, t)] = '\u03B5= ' + str(g[s][t]['edge'].voltage)

    nx.draw_networkx_edges(
        g,
        pos,
        width=0.5,
        alpha=0.5,
        edge_color="black"
    )
    nx.draw_networkx_edges(
        g,
        pos,
        edgelist=[(s, t)],
        width=0.5,
        alpha=0.5,
        edge_color="blue"
    )
    if small:
        nx.draw_networkx_edge_labels(
            g,
            pos,
            edge_labels=label_weights
        )
    plt.show()


def draw_with_current(g, s, t, small=True):
    n = g.number_of_nodes()
    g2 = nx.DiGraph()

    labels = {}
    for i in range(n):
        labels[i] = str(i)

    label_weights = {}
    for a, b in g.edges:
        edge = g[a][b]['edge']
        if a < b and edge.current < 0 or a > b and edge.current > 0:
            a, b = b, a
        g2.add_edge(a, b)
        label_weights[(a, b)] = str(np.round(abs(edge.current), 2))

    label_weights[(s, t)] = '\u03B5= ' + str(g[s][t]['edge'].voltage)
    plt.figure(figsize=(10, 8))

    pos = nx.kamada_kawai_layout(g2)
    if small:
        nx.draw_networkx_labels(
            g2,
            pos,
            labels,
            font_size=5,
            font_color="black"
        )

    node_size = 30 if small else 10
    nx.draw_networkx_nodes(
        g2,
        pos,
        nodelist=[i for i in range(n)],
        node_color="red",
        node_size=node_size,
    )

    nx.draw_networkx_nodes(
        g2,
        pos,
        nodelist=[s, t],
        node_color="blue",
        node_size=30,
    )

    arrowsize = 18 if small else 5
    nx.draw_networkx_edges(
        g2,
        pos,
        edge_color="black",
        edgelist=[(a, b) for a, b in g2.edges if a not in [s, t] or b not in [s, t]],
        arrowsize=arrowsize,
        arrowstyle=ArrowStyle.CurveFilledA(),
        width=0.5,
        alpha=0.5,
    )

    edgelist = [(s, t)] if (s, t) in g2.edges else [(t, s)]
    nx.draw_networkx_edges(
        g2,
        pos,
        edgelist=edgelist,
        edge_color='blue',
        width=0.5,
        alpha=0.5,
        arrows=False
    )

    if small:
        nx.draw_networkx_edge_labels(
            g2,
            pos,
            edge_labels=label_weights
        )
    plt.show()


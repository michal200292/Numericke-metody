import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import graph_generator


def draw_undirected_with_resistance(g, s, t, E):
    plt.figure(figsize=(10, 8))
    pos = nx.kamada_kawai_layout(g)

    labels = {}
    for i in range(g.number_of_nodes()):
        labels[i] = str(i)
    nx.draw_networkx_labels(
        g,
        pos,
        labels,
        font_size=10,
        font_color="yellow"
    )
    nx.draw_networkx_nodes(
        g,
        pos,
        nodelist=[i for i in range(g.number_of_nodes()) if i != s and i != t],
        node_color="blue",
        node_size=30,
    )

    nx.draw_networkx_nodes(
        g,
        pos,
        nodelist=[s, t],
        node_color="red",
        node_size=30,
    )
    label_weights = {}
    for a, b in g.edges:
        label_weights[(a, b)] = str(g[a][b]['weight'])
    label_weights[(s, t)] = '\u03B5= ' + str(g[s][t]['weight'])

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
        edge_color="red"
    )
    nx.draw_networkx_edge_labels(
        g,
        pos,
        edge_labels=label_weights
    )
    plt.show()


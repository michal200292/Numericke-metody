import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.patches import ArrowStyle


def draw_with_resistance(
        g: nx.Graph,
        s: int,
        t: int,
        E: float,
        small: bool = False,
        size_param: tuple[int, int] = (10, 8)
) -> None:
    """
    Draw electrical circuit with edges labeled with value of resistance of a certain edge
    """
    n = g.number_of_nodes()
    plt.figure(figsize=size_param)
    pos = g.graph['pos']
    labels = {}
    for i in range(n):
        labels[i] = str(i)

    if small:
        nx.draw_networkx_labels(
            g,
            pos,
            labels,
            font_size=10,
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
    label_weights[(s, t)] = '\u03B5= ' + str(E)

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


def draw_with_current(
        g: nx.Graph,
        s: int,
        t: int,
        E: float,
        small: bool = False,
        size_param: tuple[int, int] = (10, 8)
) -> None:
    """
        Draw electrical circuit with edges labeled with absolute value
        of current on a certain edge and direction of an edge indicating the direction
        of a current flow
    """
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

    label_weights[(s, t)] = '\u03B5= ' + str(E)
    plt.figure(figsize=size_param)

    pos = g.graph['pos']
    if small:
        nx.draw_networkx_labels(
            g2,
            pos,
            labels,
            font_size=10,
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

    arrow_size = 18 if small else 5
    nx.draw_networkx_edges(
        g2,
        pos,
        edge_color="black",
        edgelist=[(a, b) for a, b in g2.edges if a not in [s, t] or b not in [s, t]],
        arrowsize=arrow_size,
        arrowstyle=ArrowStyle.CurveFilledA(),
        width=0.5,
        alpha=0.5,
    )

    edge_list = [(s, t)] if (s, t) in g2.edges else [(t, s)]
    nx.draw_networkx_edges(
        g2,
        pos,
        edgelist=edge_list,
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


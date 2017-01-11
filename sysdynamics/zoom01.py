from matplotlib import pyplot as plt

import networkx as nx

G = nx.Graph()
G.add_node("NAV")
G.add_node("NAVSZI")
G.add_node("Minta")
G.add_node("Kiírás")
G.add_node("Raktár")
G.add_node("Vjzk")

G.add_edges_from([
    ("NAV", "NAVSZI"),
    ("Minta", "NAVSZI"),
    ("Kiírás", "NAVSZI"),
    ("Kiírás", "Minta"),
    ("NAVSZI", "Raktár"),
    ("NAVSZI", "Vjzk")
])

nx.draw_networkx(G)

plt.show()

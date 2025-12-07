import networkx as nx
from math import inf

def apsp_length(G: nx.DiGraph):
    nodes = list(G.nodes())
    n = len(nodes)
    idx = {nodes[i]: i for i in range(n)}

    dist = [[inf]*n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for u, v, w in G.edges(data="weight"):
        dist[idx[u]][idx[v]] = min(dist[idx[u]][idx[v]], w)

    for k in range(n):
        for i in range(n):
            if dist[i][k] == inf:
                continue
            for j in range(n):
                new_cost = dist[i][k] + dist[k][j]
                if new_cost < dist[i][j]:
                    dist[i][j] = new_cost

    paths = []
    for i in range(n):
        for j in range(n):
            paths.append(dist[i][j])

    return paths

"""
Floyd-Warshall Algorithm for All-Pairs Shortest Paths

Library Usage (NetworkX - storage and traversal only):
  - nx.DiGraph: Graph data structure
  - G.number_of_nodes(): Get vertex count
  - G.edges(data=True): Iterate all edges with weights

No library shortest-path algorithms are used.
All shortest-path logic is implemented from scratch.
"""
import networkx as nx
from math import inf


def apsp_length(G: nx.DiGraph):
    """
    Floyd-Warshall algorithm for All-Pairs Shortest Paths.
    Time complexity: O(V^3)
    Space complexity: O(V^2)
    """
    n = G.number_of_nodes()
    
    # Initialize distance matrix with infinity
    dist = [[inf] * n for _ in range(n)]
    
    # Distance from a node to itself is 0
    for i in range(n):
        dist[i][i] = 0
    
    # Set initial distances based on edge weights
    for u, v, data in G.edges(data=True):
        weight = data.get('weight', 1)
        dist[u][v] = weight
    
    # Floyd-Warshall: consider each vertex k as intermediate node
    for k in range(n):
        for i in range(n):
            for j in range(n):
                # If path through k is shorter, update distance
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Convert 2D matrix to flat list (matches dijkstra.py output format)
    paths_length = []
    for i in range(n):
        for j in range(n):
            paths_length.append(dist[i][j])
    
    return paths_length

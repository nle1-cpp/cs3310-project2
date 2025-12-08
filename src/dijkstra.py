"""
Dijkstra's Algorithm for All-Pairs Shortest Paths

Library Usage (NetworkX - storage and traversal only):
  - nx.DiGraph: Graph data structure
  - G.number_of_nodes(): Get vertex count
  - G.out_edges(u, data="weight"): Iterate outgoing edges with weights

No library shortest-path algorithms are used.
All shortest-path logic is implemented from scratch.
"""
from heapq import heappush, heappop
from math import inf
import networkx as nx


def apsp_length(G: nx.DiGraph):
    """
    All-Pairs Shortest Paths using repeated single-source Dijkstra.
    Runs Dijkstra V times (once from each source vertex).
    Time complexity: O(V * E log V)
    """
    paths_length = []
    n = G.number_of_nodes()
    
    # Run single-source Dijkstra from each vertex
    for source in range(n):
        distances = single_source_dijkstra(G, source)
        paths_length.extend(distances)
    
    return paths_length

def single_source_dijkstra(G: nx.DiGraph, source: int) -> list:
    """
    Single-source Dijkstra: computes shortest paths from source to ALL vertices.
    Time complexity: O(E log V)
    """
    n = G.number_of_nodes()
    dist = [inf] * n
    visited = [False] * n
    
    dist[source] = 0
    pq = [(0, source)]  # (distance, vertex)
    
    while pq:
        cur_dist, u = heappop(pq)
        
        if visited[u]:
            continue
        visited[u] = True
        
        # Relax all outgoing edges from u
        for (_, v, w) in G.out_edges(u, data="weight"):
            if visited[v]:
                continue
            
            new_dist = cur_dist + w
            if new_dist < dist[v]:
                dist[v] = new_dist
                heappush(pq, (new_dist, v))
    
    return dist

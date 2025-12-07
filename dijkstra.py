from heapq import heappush, heappop
from math import inf
import networkx as nx

def apsp_length(G: nx.DiGraph):
    paths_length = []
    nodes = list(G.nodes())
    node_to_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    for i in range(n):
        for j in range(n):
            if i == j:
                paths_length.append(0)
            else:
                start = nodes[i]
                target = nodes[j]
                path_length = single_pair_path_length(G, start, target)
                paths_length.append(path_length)
    return paths_length

def single_pair_path_length(G: nx.DiGraph, start, target) -> float:
    if start == target:
        return 0

    nodes = list(G.nodes())
    node_to_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)
    adj = [{"cost": inf, "visited": False} for _ in range(n)]

    start_idx = node_to_index[start]
    adj[start_idx]["cost"] = 0

    pq = []
    heappush(pq, (0, start))

    while pq:
        cur_cost, cur = heappop(pq)
        if cur == target:
            return cur_cost

        cur_idx = node_to_index[cur]
        if adj[cur_idx]["visited"]:
            continue

        adj[cur_idx]["visited"] = True

        for (u, v, w) in G.out_edges(cur, data="weight"):
            v_idx = node_to_index[v]
            if adj[v_idx]["visited"]:
                continue

            new_cost = cur_cost + w
            if new_cost < adj[v_idx]["cost"]:
                adj[v_idx]["cost"] = new_cost
                heappush(pq, (new_cost, v))

    return inf

from heapq import heappush, heappop
from numpy import inf
import networkx as nx 

def apsp_length(G: nx.DiGraph):
    paths_length = []
    n = G.number_of_nodes()
    for i in range(0,n):
        for j in range(0,n):
            if i == j:
                paths_length.append(0)
            else:
                path = single_pair_path_length(G,i,j)
                paths_length.append(path)

    return paths_length

def single_pair_path_length(G: nx.DiGraph, start: int, target: int) -> float:
    if start == target:
        return 0

    n = G.number_of_nodes()
    # adj[i] = {weight,prev,visited}
    adj = [{"cost":inf, "prev":-1, "visited":False} for _ in range(n)]

    pq = []
    heappush(pq, (0, start))
    adj[start]["cost"] = 0

    while len(pq) > 0:
        cur_cost, cur = heappop(pq)
        if cur == target:
            adj[target]["cost"] = cur_cost
            break

        if adj[cur]["visited"]:
            continue

        adj[cur]["visited"] = True

        edges = G.out_edges(cur,data="weight")
        for (u,v,w) in edges:
            if adj[v]["visited"]:
                continue
            
            neighbor_cost = w + adj[u]["cost"]
            if neighbor_cost >= adj[v]["cost"]:
                continue

            adj[v]["cost"] = neighbor_cost
            adj[v]["prev"] = u
            heappush(pq, (neighbor_cost, v))

    return adj[target]["cost"]

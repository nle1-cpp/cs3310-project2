import networkx as nx
import random
import time
import sys

import dijkstra as dj
import floyd_warshall as fw

OUTPUT = "runtime.csv"
MAX_VERTICES = 100
TRIALS = 5

def alg_runtime(G, callback=None):
    if callback != None:
        start_time = time.time()
        callback(G)
        return time.time() - start_time # may need to convert to ms?


def main():
    # Sanity check for Dijkstra's and Floyd-Warshall algorithms
    G = nx.gnp_random_graph(10, 0.2, directed=True)
    for (u, v) in G.edges():
        G.edges[u,v]["weight"] = random.randint(0,10)

    expected_paths = []
    exp_dict = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight")).items()
    for _,v in exp_dict:
        for _,cost in v.items():
            expected_paths.append(cost)

    dj_paths = dj.apsp_length(G)
    fw_paths = dj.apsp_length(G)

    expected_paths.sort()
    dj_paths.sort()
    fw_paths.sort()

    for i in range(0, len(expected_paths)):
        print(f"{expected_paths[i]}{dj_paths[i]}{fw_paths[i]}")
        if expected_paths[i] != dj_paths[i] or expected_paths[i] != fw_paths[i]:
            print("Path computed is incorrect")
            sys.exit()

    # Test using graphs with vertex counts of multiples 10
    # Repeat tests to mitigate experimental error
    with open(OUTPUT, "w") as f:
        f.write("#vertices,")
    
    f = open(OUTPUT, "a")
    f.write("dj,fw,\n")

    for n in range(10, MAX_VERTICES, 10):
        for i in range(0, TRIALS):
            # Generate a random graph with NetworkX that has n nodes
            # and a probability of 50% of creating an edge between each node pair
            G = nx.gnp_random_graph(n, 0.5, directed=True)

            # Write data to file
            dj_time = alg_runtime(dj.apsp_length(G))
            fw_time = alg_runtime(fw.apsp_length(G))
            f.write(f"{n},{dj_time},{fw_time}\n")

if __name__=="__main__":
    main()

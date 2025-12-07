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
    # Sanity check: compare Dijkstra's vs Floyd-Warshall (should produce identical results)
    print("Running sanity check...")
    G = nx.gnp_random_graph(10, 0.2, directed=True)
    for (u, v) in G.edges():
        G.edges[u,v]["weight"] = random.randint(1, 10)

    dj_paths = dj.apsp_length(G)
    fw_paths = fw.apsp_length(G)

    # Sort both lists to compare (order may differ due to implementation)
    dj_sorted = sorted(dj_paths)
    fw_sorted = sorted(fw_paths)

    if len(dj_sorted) != len(fw_sorted):
        print("Error: Different number of paths computed")
        sys.exit(1)

    for i in range(len(dj_sorted)):
        if dj_sorted[i] != fw_sorted[i]:
            print(f"Mismatch at index {i}: Dijkstra={dj_sorted[i]}, Floyd-Warshall={fw_sorted[i]}")
            print("Path computed is incorrect")
            sys.exit(1)
    
    print("Sanity check passed: Dijkstra and Floyd-Warshall produce identical results")

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
            for (u, v) in G.edges():
                G.edges[u,v]["weight"] = random.randint(1, 10)

            # Write data to file
            dj_time = alg_runtime(G, dj.apsp_length)
            fw_time = alg_runtime(G, fw.apsp_length)
            f.write(f"{n},{dj_time},{fw_time}\n")

if __name__=="__main__":
    main()

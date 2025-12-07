import networkx as nx
import random
import time
import sys

import dijkstra as dj
import floyd_warshall as fw

OUTPUT = "runtime.csv"
MAX_VERTICES = 100
TRIALS = 5
SPARSE_DENSITY = 0.15  # 15% edge probability (sparse)
DENSE_DENSITY = 0.50   # 50% edge probability (dense)

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

    # Test using graphs with vertex counts of multiples of 10
    # Test both sparse and dense graphs
    # Repeat tests to mitigate experimental error and compute averages
    print(f"\nRunning benchmarks ({TRIALS} trials per size)...")
    
    with open(OUTPUT, "w") as f:
        f.write("#vertices,density,dj_avg,fw_avg\n")
        
        for n in range(10, MAX_VERTICES, 10):
            # Test both sparse and dense graphs for each vertex count
            for density, density_name in [(SPARSE_DENSITY, "sparse"), (DENSE_DENSITY, "dense")]:
                dj_total = 0
                fw_total = 0
                
                for i in range(TRIALS):
                    # Generate a random directed graph with given density
                    G = nx.gnp_random_graph(n, density, directed=True)
                    for (u, v) in G.edges():
                        G.edges[u,v]["weight"] = random.randint(1, 10)

                    # Accumulate runtime for each algorithm
                    dj_total += alg_runtime(G, dj.apsp_length)
                    fw_total += alg_runtime(G, fw.apsp_length)
                
                # Compute and write average runtime
                dj_avg = dj_total / TRIALS
                fw_avg = fw_total / TRIALS
                f.write(f"{n},{density_name},{dj_avg},{fw_avg}\n")
                print(f"  n={n} ({density_name}): Dijkstra={dj_avg:.6f}s, Floyd-Warshall={fw_avg:.6f}s")

if __name__=="__main__":
    main()

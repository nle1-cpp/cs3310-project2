import networkx as nx
import random
import time
import sys

# graphing library
import pandas as pd
import matplotlib.pyplot as plt

import dijkstra as dj
import floyd_warshall as fw

OUTPUT = "runtime.csv"
MAX_VERTICES = 100
TRIALS = 5
SPARSE_DENSITY = 0.15  # 15% edge probability (sparse)
DENSE_DENSITY = 0.50   # 50% edge probability (dense)


def alg_runtime(G, callback):
    """Measure the runtime of a shortest-path APSP algorithm."""
    start_time = time.time()
    callback(G)
    return time.time() - start_time


def main():
    # ---------------------------------------------------------------
    #  Sanity check for Dijkstra's and Floyd–Warshall algorithms
    # ---------------------------------------------------------------
    print("Running sanity check...")
    G = nx.gnp_random_graph(10, 0.2, directed=True)
    for (u, v) in G.edges():
        G.edges[u,v]["weight"] = random.randint(1, 10)

    # Call student algorithms
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
        f.write("#vertices,density,dj,fw\n")
        
        for n in range(10, MAX_VERTICES, 10):
            # Test both sparse and dense graphs for each vertex count
            for density, density_name in [(SPARSE_DENSITY, "sparse"), (DENSE_DENSITY, "dense")]:
                
                for i in range(TRIALS):
                    # Generate a random directed graph with given density
                    G = nx.gnp_random_graph(n, density, directed=True)
                    for (u, v) in G.edges():
                        G.edges[u,v]["weight"] = random.randint(1, 10)

                    # Time both algorithms
                    dj_time = alg_runtime(G, dj.apsp_length)
                    fw_time = alg_runtime(G, fw.apsp_length)

                    # Write results
                    f.write(f"{n},{density_name},{dj_time},{fw_time}\n")

    # ---------------------------------------------------------------
    #  Print out runtime.csv
    # ---------------------------------------------------------------
    print("\nRuntime results from runtime.csv:")
    df = pd.read_csv(OUTPUT)
    print(df)

    # this part here is to plot the results on a graph
    avg_df = df.groupby('#vertices')[['dj','fw']].mean().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(avg_df['#vertices'], avg_df['dj'], marker='o', label='Dijkstra')
    plt.plot(avg_df['#vertices'], avg_df['fw'], marker='o', label='Floyd-Warshall')

    plt.title('APSP Algorithm Runtime Comparison')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Average Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot.png', bbox_inches='tight')


if __name__ == "__main__":
    main()

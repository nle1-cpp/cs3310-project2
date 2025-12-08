"""
APSP Algorithm Benchmarking

Library Usage (NetworkX - storage and traversal only):
  - nx.DiGraph: Graph data structure
  - nx.gnp_random_graph(): Generate random graphs
  - nx.is_weakly_connected(): Check graph connectivity
  - G.edges(): Iterate edges to assign weights

No library shortest-path algorithms are used.
All shortest-path logic is implemented from scratch in dijkstra.py and floyd_warshall.py.
"""
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


def generate_connected_graph(n, density):
    """
    Generate a random directed graph that is weakly connected.
    Keeps regenerating until a connected graph is produced.
    """
    while True:
        G = nx.gnp_random_graph(n, density, directed=True)
        if nx.is_weakly_connected(G):
            # Assign random positive weights to all edges
            for (u, v) in G.edges():
                G.edges[u, v]["weight"] = random.randint(1, 10)
            return G


def alg_runtime(G, callback=None):
    if callback != None:
        start_time = time.time()
        callback(G)
        return time.time() - start_time # may need to convert to ms?


def main():
    # ---------------------------------------------------------------
    #  Sanity check for Dijkstra's and Floyd–Warshall algorithms
    # ---------------------------------------------------------------
    print("Running sanity check...")
    G = generate_connected_graph(10, 0.3)

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
                    # Generate a random connected directed graph with given density
                    G = generate_connected_graph(n, density)

                    # Time both algorithms
                    dj_time = alg_runtime(G, dj.apsp_length)
                    fw_time = alg_runtime(G, fw.apsp_length)

    # this part here is to plot the results on a graph
    df = pd.read_csv(OUTPUT)

    # Average over densities for each vertex count
    avg_df = df.groupby('#vertices')[['dj_avg', 'fw_avg']].mean().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(avg_df['#vertices'], avg_df['dj_avg'], marker='o', label='Dijkstra')
    plt.plot(avg_df['#vertices'], avg_df['fw_avg'], marker='o', label='Floyd-Warshall')

    plt.title('APSP Algorithm Runtime Comparison')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Average Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plot.png', bbox_inches='tight')

if __name__=="__main__":
    main()

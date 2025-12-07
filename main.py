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


def alg_runtime(G, callback):
    """Measure the runtime of a shortest-path APSP algorithm."""
    start_time = time.time()
    callback(G)
    return time.time() - start_time


def main():
    # ---------------------------------------------------------------
    #  Sanity check for Dijkstra's and Floyd–Warshall algorithms
    # ---------------------------------------------------------------
    G = nx.gnp_random_graph(10, 0.2, directed=True)
    for (u, v) in G.edges():
        G.edges[u, v]["weight"] = random.randint(0, 10)

    expected_paths = []
    exp_dict = dict(nx.all_pairs_dijkstra_path_length(G, weight="weight")).items()
    for _, v in exp_dict:
        for _, cost in v.items():
            expected_paths.append(cost)

    # Call student algorithms
    dj_paths = dj.apsp_length(G)
    fw_paths = fw.apsp_length(G)

    # Sort for comparison
    expected_paths.sort()
    dj_paths.sort()
    fw_paths.sort()

    for i in range(len(expected_paths)):
        print(f"{expected_paths[i]} {dj_paths[i]} {fw_paths[i]}")
        if expected_paths[i] != dj_paths[i] or expected_paths[i] != fw_paths[i]:
            print("Path computed is incorrect")
            sys.exit()

    # ---------------------------------------------------------------
    #  Runtime testing
    # ---------------------------------------------------------------
    with open(OUTPUT, "w") as f:
        f.write("#vertices,dj,fw\n")

    with open(OUTPUT, "a") as f:
        for n in range(10, MAX_VERTICES + 1, 10):
            for _ in range(TRIALS):

                # Generate random directed graph
                G = nx.gnp_random_graph(n, 0.5, directed=True)
                for (u, v) in G.edges():
                    G.edges[u, v]["weight"] = random.randint(0, 10)

                # Time both algorithms
                dj_time = alg_runtime(G, dj.apsp_length)
                fw_time = alg_runtime(G, fw.apsp_length)

                # Write results
                f.write(f"{n},{dj_time},{fw_time}\n")

    # ---------------------------------------------------------------
    #  Print out runtime.csv
    # ---------------------------------------------------------------
    print("\nRuntime results from runtime.csv:")
    df = pd.read_csv(OUTPUT)
    print(df)

    # this part here is to plot the results on a graph
    avg_df = df.groupby('#vertices').mean().reset_index()

    plt.figure(figsize=(8, 5))
    plt.plot(avg_df['#vertices'], avg_df['dj'], marker='o', label='Dijkstra')
    plt.plot(avg_df['#vertices'], avg_df['fw'], marker='o', label='Floyd-Warshall')

    plt.title('APSP Algorithm Runtime Comparison')
    plt.xlabel('Number of Vertices')
    plt.ylabel('Average Runtime (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()

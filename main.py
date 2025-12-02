from network import nx 
import time

OUTPUT = "runtime.csv"
MAX_VERTICES = 100
TRIALS = 5

def alg_runtime(callback=None):
    if callback != None:
        start_time = time.time()
        callback
        return time.time() - start_time # may need to convert to ms?


def main():
# Sanity check for Dijkstra's and Floyd-Warshall algorithms
    test_nodes = []
    test_edges = [
        (1,2,{"weight":-1}),
    ]
    expected_path = []

    G = nx.DiGraph()
    G.add_nodes_from(test_nodes)
    G.add_edges_from(test_edges)

    dj_path = G.dijkstra()
    fw_path = G.floyd_warshall()

    if len(expected_path) == len(dj_path) and len(expected_path) == len(fw_path):
       for i in range(0, len(expected_path)):
            if expected_path[i] != dj_path[i] or expected_path[i] != fw_path[i]:
                print("Path computed is incorrect")
                exit


# Test using graphs with vertex counts of multiples 10
# Repeat tests to mitigate experimental error
    with open(OUTPUT, "w") as f:
        f.write("#vertices,")
    
    f = open(OUTPUT, "a")
    for i in range(0,TRIALS):
        f.write(f"dj{i},fw{i},")
    f.write("\n")

    for n in range(0, MAX_VERTICES, 10):
        for i in range(0, TRIALS):
            G = generate_graph(n) 
            f.write(n)
            f.write(alg_runtime(G.dijkstra(start, end)) + ",")
            f.write(alg_runtime(G.floyd_warshall(start, end)) + ",")
        f.write("\n")

if __name__=="__main__":
    main()

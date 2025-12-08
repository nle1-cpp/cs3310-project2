# CS 3310 Project 2

## Team Members

- Nathan Le
- Kevin Wenas
- Adam Robles
- Chung Tran

## Description

This project implements and compares the runtime performance of two APSP algorithms:

1. **Repeated Dijkstra's Algorithm** — Runs single-source Dijkstra from every vertex
   - Time Complexity: O(V × E log V)
   
2. **Floyd-Warshall Algorithm** — Dynamic programming approach using intermediate vertices
   - Time Complexity: O(V³)

## Project Structure

```
cs3310-project2/
├── README.md
├── pyproject.toml
├── runtime.csv          # Benchmark results
├── plot.png             # Runtime comparison graph
└── src/
    ├── main.py          # Benchmarking driver
    ├── dijkstra.py      # Dijkstra's algorithm (from scratch)
    └── floyd_warshall.py # Floyd-Warshall algorithm (from scratch)
```

## Requirements

- Python 3.8+
- NetworkX
- Pandas
- Matplotlib

Install dependencies:
```bash
pip install networkx pandas matplotlib
```

Or using the project file:
```bash
pip install -e .
```

## Usage

Run the benchmark:
```bash
cd src
python main.py
```

This will:
1. Run a sanity check to verify both algorithms produce identical results
2. Benchmark both algorithms on graphs with n = 10, 20, 30, ..., 90 vertices
3. Test both sparse (15% density) and dense (50% density) graphs
4. Run 5 trials per configuration and compute averages
5. Save results to `runtime.csv` and generate `plot.png`

## Library Usage Documentation

**NetworkX is used ONLY for graph storage and basic traversal — no shortest-path algorithms are called.**

### Allowed NetworkX Functions Used

| File | Function | Purpose |
|------|----------|---------|
| `main.py` | `nx.DiGraph` | Graph data structure |
| `main.py` | `nx.gnp_random_graph()` | Generate random test graphs |
| `main.py` | `nx.is_weakly_connected()` | Verify graph connectivity |
| `main.py` | `G.edges()` | Iterate edges to assign weights |
| `dijkstra.py` | `G.number_of_nodes()` | Get vertex count |
| `dijkstra.py` | `G.out_edges()` | Iterate outgoing edges with weights |
| `floyd_warshall.py` | `G.number_of_nodes()` | Get vertex count |
| `floyd_warshall.py` | `G.edges()` | Iterate all edges with weights |

### Disallowed Functions NOT Used

The following NetworkX shortest-path functions are **not** used anywhere in this project:
- `nx.shortest_path()`
- `nx.all_pairs_dijkstra_path_length()`
- `nx.floyd_warshall()`
- `nx.single_source_dijkstra()`

All shortest-path logic is implemented from scratch in `dijkstra.py` and `floyd_warshall.py`.

## Algorithm Implementations

### Dijkstra's Algorithm (`dijkstra.py`)

- Uses Python's `heapq` for the priority queue
- Implements edge relaxation manually
- Runs single-source Dijkstra V times (once from each vertex)

### Floyd-Warshall Algorithm (`floyd_warshall.py`)

- Uses a 2D distance matrix initialized with edge weights
- Implements the classic triple-nested loop: for each intermediate vertex k, update all pairs (i, j)
- Returns distances in the same format as Dijkstra for comparison

## Output

- **runtime.csv**: Raw benchmark data with columns `#vertices`, `density`, `dj` (Dijkstra time), `fw` (Floyd-Warshall time)
- **plot.png**: Graph comparing average runtime vs. number of vertices

## Sample Output

```
Running sanity check...
Sanity check passed: Dijkstra and Floyd-Warshall produce identical results

Running benchmarks (5 trials per size)...
Testing vertex counts: 10, 20, ..., 90
Densities: sparse (15%), dense (50%)
------------------------------------------------------------
n= 10, sparse: Dijkstra avg=0.000062s, Floyd-Warshall avg=0.000058s
n= 10, dense : Dijkstra avg=0.000176s, Floyd-Warshall avg=0.000058s
...

SUMMARY: Average Runtime per Vertex Count (across all trials and densities)
------------------------------------------------------------
Vertices   Dijkstra (s)    Floyd-Warshall (s)
------------------------------------------------------------
10         0.000127        0.000060          
20         0.000760        0.000362          
...
```


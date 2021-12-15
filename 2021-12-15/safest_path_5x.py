#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np
import igraph


def get_input():
    all_rows = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        row = [int(x) for x in line]
        all_rows.append(row)
    risk_mtx = np.array(all_rows, dtype=int)
    return risk_mtx


def coords2idx(c, shape):
    """ (2,3) --> 2 * cols + 3 """
    assert len(c) == 2
    cols = shape[1]
    return c[0] * cols + c[1]


def idx2coords(i, shape):
    """ i --> (x,y) such that coords2idx((x,y), shape) == i """
    assert type(i) == int
    cols = shape[1]
    return (i // cols, i % cols)


def build_risk_graph(m):
    g = igraph.Graph(directed=True)
    rows, cols = m.shape
    g.add_vertices(rows * cols)
    # Create a list of edges and their weights
    edges = []
    weights = []
    for i in range(rows):
        for j in range(cols):
            if i > 0:
                edges.append([coords2idx((i-1,j), m.shape), coords2idx((i,j), m.shape)])
                weights.append(m[i,j])
            if i < rows - 1:
                edges.append([coords2idx((i+1,j), m.shape), coords2idx((i,j), m.shape)])
                weights.append(m[i,j])
            if j > 0:
                edges.append([coords2idx((i,j-1), m.shape), coords2idx((i,j), m.shape)])
                weights.append(m[i,j])
            if j < cols - 1:
                edges.append([coords2idx((i,j+1), m.shape), coords2idx((i,j), m.shape)])
                weights.append(m[i,j])
    g.add_edges(edges, attributes={"weight":weights})
    g.vs["weight"] = [m[i,j] for i in range(rows) for j in range(cols)]
    return g


def increment_wrap9(m, inc=1):
    assert inc >= 0
    m = m.copy()
    if inc == 0:
        return m.copy()
    m = (m - 1) + inc
    m = m % 9
    m = m + 1
    return m


def expand_5x(m):
    bigrow0 = np.concatenate([increment_wrap9(m,i) for i in range(5)], axis=1)
    bigmtx = np.concatenate([increment_wrap9(bigrow0, i) for i in range(5)], axis=0)
    return bigmtx


#############################################################################

risk_mtx = get_input()
risk_mtx = expand_5x(risk_mtx)

g = build_risk_graph(risk_mtx)
# print(g)

# Find safest (shortest) path
rows, cols = risk_mtx.shape
start = coords2idx((0, 0), risk_mtx.shape)
end = coords2idx((rows-1, cols-1), risk_mtx.shape)
s_costs = g.shortest_paths(source=start, target=end, weights="weight")
s_paths = g.get_shortest_paths(start, to=end, weights="weight")
s_path = s_paths[0]
print("Shortest path from %s to %s:" % (str((0,0)), str((rows-1,cols-1))))
print([(idx2coords(i, risk_mtx.shape), g.vs[i]["weight"]) for i in s_path])
print("Cost of shortest path:", int(s_costs[0][0]))

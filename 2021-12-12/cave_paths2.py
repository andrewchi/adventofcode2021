#!/home/andrew/.envs/venv38/bin/python3

import sys
import igraph


def read_input():
    edge_list = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        edge_list.append(line.split("-"))
    return edge_list


def create_graph(edge_list):
    vertex_set = set()
    for v,w in edge_list:
        vertex_set.add(v)
        vertex_set.add(w)
    vertex_names = sorted(vertex_set)
    vertex_ids = {vertex_names[i]:i for i in range(len(vertex_names))}
    edges = [(vertex_ids[v], vertex_ids[w]) for v,w in edge_list]
    g = igraph.Graph(edges)
    g.vs["name"] = vertex_names
    return g


def too_many_visits(path):
    """Have we visited more than one small cave twice already?
    Or have we visited "start" or "end" more than once?
    """
    if path.count("start") > 1:
        return True
    if path.count("end") > 1:
        return True
    small_caves = [p for p in path if p.islower()]
    if len(small_caves) > len(set(small_caves)) + 1:
        return True
    return False


def cave_search(v_now, v_end, path_history=[]):
    paths_found = []
    path_now = path_history + [v_now["name"]]
    if too_many_visits(path_now):
        pass
    elif v_now == v_end:
        paths_found.append(path_now)
    else:
        for v_next in v_now.neighbors():
            paths_found.extend(cave_search(v_next, v_end, path_now))
    return paths_found


###########################################################

edge_list = read_input()
g = create_graph(edge_list)
print(g)

v_start = g.vs.find(name="start")
v_end = g.vs.find(name="end")
print("Start vertex:", v_start)
print("End vertex:", v_end)

print("Neighbors of the start vertex:", v_start.neighbors())
print("Neighbors of the end vertex:", v_end.neighbors())

paths_found = cave_search(v_start, v_end)
for p in paths_found:
    print(",".join(p))
print("Number of paths:", len(paths_found))

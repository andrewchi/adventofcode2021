#!/home/andrew/.envs/venv38/bin/python3


import sys
import numpy as np


def read_input():
    vent_lines = []
    for line in sys.stdin:
        halves = (x.strip() for x in line.strip().split("->"))
        points = [[int(x) for x in y.split(",")] for y in halves]
        vent_lines.append(points)
    return vent_lines


def is_rook_move(vent_line):
    v = vent_line
    return (v[0][0] == v[1][0]) or (v[0][1] == v[1][1])


def integer_points(vent_line):
    v = vent_line
    if not is_rook_move(v):
        return []
    points = []
    x_begin = min(v[0][0], v[1][0])
    x_end = max(v[0][0], v[1][0]) + 1
    y_begin = min(v[0][1], v[1][1])
    y_end = max(v[0][1], v[1][1]) + 1
    for x in range(x_begin, x_end):
        for y in range(y_begin, y_end):
            points.append([x,y])
    return points


def infer_grid_shape(vent_lines):
    x_max = -1
    y_max = -1
    for v in vent_lines:
        for p in v:
            x_max = max(x_max, p[0])
            y_max = max(y_max, p[1])
    return [y_max + 1, x_max + 1]


# Read in vent lines and infer grid shape
vent_lines = read_input()
grid_shape = infer_grid_shape(vent_lines)
#print(vent_lines)
print("Grid shape:", grid_shape)

# Create grid and weight each point by number of vents
grid = np.zeros(grid_shape, dtype=int)
for v in vent_lines:
    for x,y in integer_points(v):
        grid[y, x] += 1
#print(grid)

# Compute the number of points with weight at least 2
dangerous_points = np.sum(grid >= 2)
print("Number of dangerous points:", dangerous_points)

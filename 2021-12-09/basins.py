#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np
import itertools
import collections

def get_input():
    matrix = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        digits = [int(c) for c in line]
        matrix.append(digits)
    return np.array(matrix, dtype=int)

heightmap = get_input()
#print("Height map:")
#print(heightmap)

# Is each height more than the adjacent height (up, down, left, right)?
is_more_than_up = np.zeros(heightmap.shape, dtype=bool)
is_more_than_up[0,:] = False
is_more_than_up[1:,:] = heightmap[1:,:] > heightmap[:-1,:]
#print("is_more_than_up:")
#print(is_more_than_up)

is_more_than_down = np.zeros(heightmap.shape, dtype=bool)
is_more_than_down[-1,:] = False
is_more_than_down[:-1,:] = heightmap[:-1,:] > heightmap[1:,:]
#print("is_more_than_down:")
#print(is_more_than_down)

is_more_than_left = np.zeros(heightmap.shape, dtype=bool)
is_more_than_left[:,0] = False
is_more_than_left[:,1:] = heightmap[:,1:] > heightmap[:,:-1]
#print("is_more_than_left:")
#print(is_more_than_left)

is_more_than_right = np.zeros(heightmap.shape, dtype=bool)
is_more_than_right[:,-1] = False
is_more_than_right[:,:-1] = heightmap[:,:-1] > heightmap[:,1:]
#print("is_more_than_right:")
#print(is_more_than_right)

# Create downward pointers
downward_ptr = {}
low_points = []
rows, cols = heightmap.shape
for i,j in itertools.product(range(rows), range(cols)):
    if heightmap[i,j] == 9:
        continue
    if is_more_than_up[i,j]:
        downward_ptr[(i, j)] = (i-1, j)
    elif is_more_than_down[i,j]:
        downward_ptr[(i, j)] = (i+1, j)
    elif is_more_than_left[i,j]:
        downward_ptr[(i, j)] = (i, j-1)
    elif is_more_than_right[i,j]:
        downward_ptr[(i, j)] = (i, j+1)
    else:
        print("minimum at position (%d,%d): %d" % (i, j, heightmap[i,j]))
        downward_ptr[(i,j)] = (i,j)
        low_points.append((i,j))
#print(downward_ptr)


# Run union-find (disjoint set) on the downward pointers
def union_find(input_dictionary):
    d = input_dictionary.copy()
    for x in d:
        find_and_set_parent(x, d)
    return d

def find_and_set_parent(x, d):
    if d[x] == x:
        return x
    else:
        d[x] = find_and_set_parent(d[x], d)
        return d[x]

basin_ids = union_find(downward_ptr)

# Compute basin sizes
basin_sizes = collections.defaultdict(int)
for low_point in basin_ids.values():
    basin_sizes[low_point] += 1
#print(basin_sizes)

# basins by size
basins_by_size = sorted(basin_sizes.values(), reverse=True)
print("Basins by size:", basins_by_size)
b = basins_by_size
print("Product of the top 3 basins:", b[0] * b[1] * b[2])

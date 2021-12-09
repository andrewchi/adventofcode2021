#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np

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

# Is each height less than the adjacent height (up, down, left, right)?
rows, cols = heightmap.shape

is_less_than_up = np.zeros(heightmap.shape, dtype=bool)
is_less_than_up[0,:] = True
is_less_than_up[1:,:] = heightmap[1:,:] < heightmap[:-1,:]
#print("is_less_than_up:")
#print(is_less_than_up)

is_less_than_down = np.zeros(heightmap.shape, dtype=bool)
is_less_than_down[-1,:] = True
is_less_than_down[:-1,:] = heightmap[:-1,:] < heightmap[1:,:]
#print("is_less_than_down:")
#print(is_less_than_down)

is_less_than_left = np.zeros(heightmap.shape, dtype=bool)
is_less_than_left[:,0] = True
is_less_than_left[:,1:] = heightmap[:,1:] < heightmap[:,:-1]
#print("is_less_than_left:")
#print(is_less_than_left)

is_less_than_right = np.zeros(heightmap.shape, dtype=bool)
is_less_than_right[:,-1] = True
is_less_than_right[:,:-1] = heightmap[:,:-1] < heightmap[:,1:]
#print("is_less_than_right:")
#print(is_less_than_right)

low_points = is_less_than_up & is_less_than_down \
    & is_less_than_left & is_less_than_right
#print("low_points:")
#print(low_points)

risk_level = (heightmap + 1) * low_points.astype(int)
print("Sum of risk levels:", np.sum(risk_level))

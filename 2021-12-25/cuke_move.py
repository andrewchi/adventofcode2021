#!/usr/bin/env python3

import sys
import numpy as np


CUKE_CODE = {'.': 0, '>': 1, 'v': 2, 0:'.', 1:'>', 2:'v'}


def get_input():
    cukes_all = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        cukes_all.append([CUKE_CODE[c] for c in line])
    cukes = np.array(cukes_all, dtype=int)
    return cukes


def move_cukes(cukes):
    """Move east-facing herd, then south-facing herd."""

    cukes2 = cukes.copy()

    # East-facing herd
    spaces = (cukes == CUKE_CODE['.'])
    east_movable_cukes = (cukes == CUKE_CODE['>']) & np.roll(spaces, -1, axis=1)
    cukes2[east_movable_cukes] = CUKE_CODE['.']
    cukes2[np.roll(east_movable_cukes, 1, axis=1)] = CUKE_CODE['>']

    # South-facing herd
    spaces = (cukes2 == CUKE_CODE['.'])
    south_movable_cukes = (cukes2 == CUKE_CODE['v']) & np.roll(spaces, -1, axis=0)
    cukes2[south_movable_cukes] = CUKE_CODE['.']
    cukes2[np.roll(south_movable_cukes, 1, axis=0)] = CUKE_CODE['v']

    return cukes2


def print_cukes(cukes):
    for row in cukes:
        print("".join(CUKE_CODE[n] for n in row))


############################################################################


cukes = get_input()
print("Initial state:")
print_cukes(cukes)

steps = 0
cukes_old = None
while not np.all(cukes == cukes_old):
    cukes_old = cukes
    cukes = move_cukes(cukes)
    steps += 1
    #print("After step %d:" % steps)
    #print_cukes(cukes)
print("Number of steps to convergence:", steps)

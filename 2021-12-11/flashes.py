#!/usr/bin/env python3


import sys
import numpy as np


def read_input():
    all_rows = []
    for line in sys.stdin:
        row = [int(x) for x in line.strip()]
        all_rows.append(row)
    octopuses = np.array(all_rows, dtype=int)
    return octopuses


def shift2d_x(mtx, dx):
    "Shift entire matrix dx right (or left if dx is negative)"
    assert abs(dx) <= mtx.shape[1]
    if dx == 0:
        return mtx.copy()
    mtx2 = np.zeros(mtx.shape, dtype=int)
    if dx > 0:
        mtx2[:, dx:] = mtx[:, :-dx]
    else:  # dx < 0
        mtx2[:, :dx] = mtx[:, -dx:]
    return mtx2


def shift2d_y(mtx, dy):
    "Shift entire matrix dy down (or up if dy is negative)"
    assert abs(dy) <= mtx.shape[0]
    if dy == 0:
        return mtx.copy()
    mtx2 = np.zeros(mtx.shape, dtype=int)
    if dy > 0:
        mtx2[dy:, :] = mtx[:-dy, :]
    else:  # dy < 0
        mtx2[:dy, :] = mtx[-dy:, :]
    return mtx2


def shift2d(mtx, dx, dy):
    "Shift entire matrix dx right, dy down, and zero-fill"
    mtx_x = shift2d_x(mtx, dx)
    mtx_xy = shift2d_y(mtx_x, dy)
    return mtx_xy


def can_flash(mtx):
    """"Returns a boolean matrix of flashing entries"""
    return mtx > 9


def splash_pattern(flash_mtx):
    """Takes a boolean matrix of flashing entries and returns integer matrix
    splash pattern (of energy boosts)"""
    fm = flash_mtx
    splash_mtx = np.zeros(fm.shape, dtype=int)
    shifts = [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]
    for shift in shifts:
        splash_mtx += shift2d(flash_mtx, shift[0], shift[1])
    return splash_mtx


def exec_flashes(mtx, all_flashes=None):
    """
    Execute the flash convergence part of the time step.

      - Any octopus with an energy level greater than 9 flashes. This increases
        the energy level of all adjacent octopuses by 1, including octopuses
        that are diagonally adjacent. If this causes an octopus to have an
        energy level greater than 9, it also flashes. This process continues as
        long as new octopuses keep having their energy level increased beyond 9.
        (An octopus can only flash at most once per step.)

      - Finally, any octopus that flashed during this step has its energy level
        set to 0, as it used all of its energy to flash.

    Return the tuple (new_matrix, flash_count)
    """
    if all_flashes is None:
        all_flashes = np.zeros(mtx.shape, dtype=bool)
    if np.sum(can_flash(mtx)) == 0:
        return mtx, all_flashes
    else:
        new_flashes = can_flash(mtx)
        new_mtx = mtx + splash_pattern(new_flashes)
        all_flashes |= new_flashes
        new_mtx[all_flashes] = 0
        return exec_flashes(new_mtx, all_flashes)


def time_step(mtx):
    """
    You can model the energy levels and flashes of light in steps. During a
    single step, the following occurs:

      - First, the energy level of each octopus increases by 1.

      - Then, any octopus with an energy level greater than 9 flashes. This
        increases the energy level of all adjacent octopuses by 1, including
        octopuses that are diagonally adjacent. If this causes an octopus to
        have an energy level greater than 9, it also flashes. This process
        continues as long as new octopuses keep having their energy level
        increased beyond 9. (An octopus can only flash at most once per step.)

      - Finally, any octopus that flashed during this step has its energy level
        set to 0, as it used all of its energy to flash.

    Return the tuple (new_matrix, all_flashes)
    """
    mtx_new, all_flashes = exec_flashes(mtx + 1)
    return mtx_new, all_flashes


################# main program ###############

octopuses = read_input()
#print(octopuses)

# Test out shifting
# for dx in [-1, 0, 1]:
#     for dy in [-1, 0, 1]:
#         print("Shifted dx=%d and dy=%d:" % (dx, dy))
#         print(shift2d(octopuses, dx, dy))

# Test out energy splash pattern (given a flash pattern)
# m = octopuses + 2
# print("Original:")
# print(m)
# fm = can_flash(m)
# print("Flash pattern:")
# print(fm)
# sm = splash_pattern(fm)
# print("Splash pattern:")
# print(sm)

# Run 100 steps
NUM_STEPS=100
m = octopuses
flash_count = 0
print("Before any steps:")
print(m)
for i in range(NUM_STEPS):
    m, flashes = time_step(m)
    flash_count += np.sum(flashes)
    print("\nAfter step %d:" % (i+1))
    print(m)
    #print(flashes.astype(int))

print("\nTotal number of flashes:", flash_count)

#!/usr/bin/env python3

import sys
import numpy as np

def get_input():
    coordinates = []
    fold_sequence = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("fold along"):
            fold_fields = line.split()[2].split("=")
            axis = fold_fields[0]
            value = int(fold_fields[1])
            fold_sequence.append((axis, value))
        else:
            assert "," in line
            xy = [int(x) for x in line.split(",")]
            coordinates.append(xy)
    coordinates = np.array(coordinates, dtype=int)
    return coordinates, fold_sequence


def infer_paper_shape(dots):
    assert dots.shape[1] == 2
    x_max = np.max(dots[:,0])
    y_max = np.max(dots[:,1])
    return (x_max+1, y_max+1)


def do_fold(dots, fold):
    direction = fold[0]
    crease = fold[1]
    if direction == 'x':
        return do_fold_x(dots, crease)
    elif direction == 'y':
        return do_fold_y(dots, crease)
    else:
        return None


def do_fold_x(dots, crease):
    dots_x = dots[:,0]
    dots_x_reflect = (2 * crease) - dots_x
    dots_x_folded = np.minimum(dots_x, dots_x_reflect)
    dots_new = dots.copy()
    dots_new[:,0] = dots_x_folded
    return dots_new


def do_fold_y(dots, crease):
    dots_y = dots[:,1]
    dots_y_reflect = (2 * crease) - dots_y
    dots_y_folded = np.minimum(dots_y, dots_y_reflect)
    dots_new = dots.copy()
    dots_new[:,1] = dots_y_folded
    return dots_new


def dedup_dots(dots):
    return np.unique(dots, axis=0)


###################################################################

dots, fold_sequence = get_input()
print("Dot coordinates:", dots, "\nLength:", len(dots))
print("Fold sequence:", fold_sequence)
print("Inferred paper shape:", infer_paper_shape(dots))

for fold in fold_sequence:
    dots = do_fold(dots, fold)
    print("\nAfter fold:", fold)
    print(dots, "\nLength:", len(dots))
    dots = dedup_dots(dots)
    print("Deduplicated:")
    print(dots, "\nLength:", len(dots))
    break

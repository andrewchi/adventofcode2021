#!/usr/bin/env python3

import sys

def read_binary_diagnostic():
    diagnostic_mtx = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        bits_list = [int(x) for x in list(line)]
        diagnostic_mtx.append(bits_list)
    # check dimensions
    lengths = [len(row) for row in diagnostic_mtx]
    assert max(lengths) == min(lengths)
    return diagnostic_mtx

def get_shape(mtx):
    rows = len(mtx)
    if rows > 0:
        cols = len(mtx[0])
    else:
        cols = 0
    return (rows, cols)

def most_common_bit(mtx, col, tie_value=1):
    col_as_list = [row[col] for row in mtx]
    if sum(col_as_list) == len(col_as_list) / 2:
        return tie_value
    elif sum(col_as_list) > len(col_as_list) / 2:
        return 1
    else:
        return 0

def least_common_bit(mtx, col):
    return 1 - most_common_bit(mtx, col)

def get_O2_row(mtx, startcol=0):
    rows, cols = get_shape(mtx)
    if rows == 1:
        return mtx[0]
    assert startcol < cols
    mcb = most_common_bit(mtx, startcol)
    reduced_mtx = [row for row in mtx if row[startcol] == mcb]
    # print("O2 reduced matrix:", reduced_mtx)
    return get_O2_row(reduced_mtx, startcol+1)

def get_CO2_row(mtx, startcol=0):
    rows, cols = get_shape(mtx)
    if rows == 1:
        return mtx[0]
    assert startcol < cols
    lcb = least_common_bit(mtx, startcol)
    reduced_mtx = [row for row in mtx if row[startcol] == lcb]
    # print("CO2 reduced matrix:", reduced_mtx)
    return get_CO2_row(reduced_mtx, startcol+1)

def row2int(row):
    return int("".join(str(b) for b in row), 2)

d_mtx = read_binary_diagnostic()
d_O2 = row2int(get_O2_row(d_mtx))
d_CO2 = row2int(get_CO2_row(d_mtx))
print("O2 generator rating:", d_O2, bin(d_O2))
print("CO2 scrubber rating:", d_CO2, bin(d_CO2))
print("O2 rating * CO2 rating:", d_O2 * d_CO2)

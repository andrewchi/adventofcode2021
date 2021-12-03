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

def most_common_bit(mtx, col):
    col_as_list = [row[col] for row in mtx]
    if sum(col_as_list) > len(col_as_list) / 2:
        return 1
    else:
        return 0

def least_common_bit(mtx, col):
    return 1 - most_common_bit(mtx, col)

def gamma_rate(mtx):
    rows, cols = get_shape(mtx)
    gamma_bits = [most_common_bit(mtx, col) for col in range(cols)]
    gamma_str = "".join(str(b) for b in gamma_bits)
    return int(gamma_str, 2)

def epsilon_rate(mtx):
    rows, cols = get_shape(mtx)
    return 2**cols - 1 - gamma_rate(mtx)

d_mtx = read_binary_diagnostic()
d_gamma = gamma_rate(d_mtx)
d_epsilon = epsilon_rate(d_mtx)
print("Gamma rate:", d_gamma, bin(d_gamma))
print("Epsilon rate:", d_epsilon, bin(d_epsilon))
print("Gamma * Epsilon:", d_gamma * d_epsilon)

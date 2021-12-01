#!/usr/bin/env python3

import sys
import collections
from itertools import islice

# Helper function from https://docs.python.org/3/library/itertools.html
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) -> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n), maxlen=n)
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window.append(x)
        yield tuple(window)


# Helper function: get number of increases in a numerical sequence
def count_increases(L):
    n_increases = 0
    for i in range(0, len(L)-1):
        print(L[i:i+2], "increase =", L[i] < L[i+1])
        if L[i] < L[i+1]:
            n_increases += 1
    return n_increases


# Get array of depths from stdin
depths = []
for line in sys.stdin:
    if len(line.strip()) == 0:
        continue
    depths.append(int(line.strip()))

# Get sliding windows of size 3 and find the sums
depth_w3_sums = [sum(w) for w in sliding_window(depths, 3)]

# Count the number of increases in the numerical sequence
print("Number of increases:", count_increases(depth_w3_sums))

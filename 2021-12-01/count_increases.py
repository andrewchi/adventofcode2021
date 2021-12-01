#!/usr/bin/env python3

import sys
import collections

# Get array of depths from stdin
depths = []
for line in sys.stdin:
    if len(line.strip()) == 0:
        continue
    depths.append(int(line.strip()))

# Count the number of increases in the numerical sequence
n_increases = 0
for i in range(0, len(depths)-1):
    print(depths[i:i+2], "increase =", depths[i] < depths[i+1])
    if depths[i] < depths[i+1]:
        n_increases += 1
print("Number of increases:", n_increases)

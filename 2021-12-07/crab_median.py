#!/home/andrew/.envs/venv38/bin/python3

# We just want the median of the inputs as the optimal position
# https://math.stackexchange.com/questions/113270/the-median-minimizes-the-sum-of-absolute-deviations-the-ell-1-norm

import sys
import numpy as np

crabs = np.array([int(x) for x in sys.stdin.read().strip().split(",")])

#print("Crab positions:", crabs)
crab_median = round(np.median(crabs))
print("Median:", crab_median)

total_fuel = np.sum(np.abs(crabs - crab_median))
print("Sum of distances (i.e., total fuel):", total_fuel)

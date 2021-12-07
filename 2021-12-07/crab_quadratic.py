#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np

crabs = np.array([int(x) for x in sys.stdin.read().strip().split(",")])
crab_min = np.min(crabs)
crab_max = np.max(crabs)

print("Crab positions:", crabs)
print("Crab min:", crab_min)
print("Crab max:", crab_max)

# Compute fuel costs
fuel_costs = []
positions = np.arange(crab_min, crab_max+1, dtype=int)
for pos in positions:
    L1 = np.abs(crabs - pos)
    fuel = L1 * (L1 + 1) / 2
    fuel_costs.append(np.sum(fuel))
fuel_costs = np.array(fuel_costs, dtype=int)
print("Crab positions:\n", positions)
print("Fuel costs:\n", fuel_costs)

# Get the minimum
optimal_idx = np.argmin(fuel_costs)
print("Optimal position:", positions[optimal_idx])
print("Fuel cost:", fuel_costs[optimal_idx])

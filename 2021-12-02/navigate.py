#!/usr/bin/env python3

import sys

# Read in sequence of moves
move_list = []
for line in sys.stdin:
    fields = line.strip().split()
    if len(fields) != 2:
        continue
    direction = fields[0]
    distance = int(fields[1])
    move_list.append((direction, distance))
# print(move_list)

# Calculate final position
x_pos = 0
y_pos = 0
for move in move_list:
    if move[0] == "forward":
        x_pos += move[1]
    elif move[0] == "up":
        y_pos += move[1]
    elif move[0] == "down":
        y_pos -= move[1]
    else:
        raise ValueError("Invalid move direction:", move[0])
print("Final position:", (x_pos, -y_pos))
print("Product:", x_pos * (-y_pos))

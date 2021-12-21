#!/usr/bin/env python3

import sys

def get_input():
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("Player 1 starting position:"):
            p1_start = int(line.split()[-1])
        elif line.startswith("Player 2 starting position:"):
            p2_start = int(line.split()[-1])
    return p1_start, p2_start


class DeterministicDie(object):
    def __init__(self):
        self.state = 1
        self.n_rolls = 0
    def roll(self):
        self.n_rolls += 1
        r = self.state
        self.state = (r % 100) + 1
        return r


def take_turn(pos, die):
    """Roll 3 times and move to new position.  Return new position."""
    movement = 0
    for i in range(3):
        movement += die.roll()
    return ((pos - 1 + movement) % 10) + 1

##############################################################################

p1_start, p2_start = get_input()
print("Player 1 start:", p1_start)
print("Player 2 start:", p2_start)

# Play game
dd = DeterministicDie()
positions = [p1_start, p2_start]
scores = [0, 0]
whose_turn = 0
win_threshold = 1000
while max(scores) < win_threshold:
    new_pos = take_turn(positions[whose_turn], dd)
    scores[whose_turn] += new_pos
    positions[whose_turn] = new_pos
    whose_turn = (whose_turn + 1) % len(positions)

print("Winning player points:", max(scores))
print("Losing player points:", min(scores))
print("Die number of rolls:", dd.n_rolls)
print("Losing points x rolls =", min(scores) * dd.n_rolls)

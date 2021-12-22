#!/usr/bin/env python3

import collections
import itertools
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


# Distribution of universes given 3 rolls of the dirac dice in sequence
TRIPLE_DICE_DISTR = collections.defaultdict(int)
for roll3x in itertools.product([1,2,3], repeat=3):
    TRIPLE_DICE_DISTR[sum(roll3x)] += 1


# Minimum score required to win
WIN_THRESHOLD = 21


# Special game states for player1win and player2win
# Normally, the game state is the 5-tuple:
#   p1_position: 1 - 10
#   p2_position: 1 - 10
#   p1_score: 0 - 20
#   p2_score: 0 - 20
#   whose_turn: 1 or 2
# We have two special game states that represent when a player has won.
PLAYER1WIN = (0,0,WIN_THRESHOLD,0,0)
PLAYER2WIN = (0,0,0,WIN_THRESHOLD,0)


def initialize_universes(p1_start, p2_start):
    """
    Map each possible game state -> # universes
    where the game state is the 5-tuple:
    p1_position: 1 - 10
    p2_position: 1 - 10
    p1_score: 0 - 20
    p2_score: 0 - 20
    whose_turn: 1 or 2
    """
    universes = collections.defaultdict(int)
    universes[(p1_start, p2_start, 0, 0, 1)] = 1
    return universes


def take_turn(game_state, triple_roll):
    assert game_state != PLAYER1WIN
    assert game_state != PLAYER2WIN
    p1_pos, p2_pos, p1_score, p2_score, whose_turn = game_state
    if whose_turn == 1:
        p1_pos_new = ((p1_pos - 1 + triple_roll) % 10) + 1
        p1_score_new = p1_score + p1_pos_new
        if p1_score_new >= WIN_THRESHOLD:
            game_state_new = PLAYER1WIN
        else:
            game_state_new = (p1_pos_new, p2_pos, p1_score_new, p2_score, 2)
    elif whose_turn == 2:
        p2_pos_new = ((p2_pos - 1 + triple_roll) % 10) + 1
        p2_score_new = p2_score + p2_pos_new
        if p2_score_new >= WIN_THRESHOLD:
            game_state_new = PLAYER2WIN
        else:
            game_state_new = (p1_pos, p2_pos_new, p1_score, p2_score_new, 1)
    return game_state_new


def advance_universes(universes, tdd=TRIPLE_DICE_DISTR):
    """Play the universes forward 1 turn (3 rolls), except for universes that
    are already in the "player1win" or "player2win" state."""
    universes_next = collections.defaultdict(int)
    if PLAYER1WIN in universes:
        universes_next[PLAYER1WIN] = universes[PLAYER1WIN]
    if PLAYER2WIN in universes:
        universes_next[PLAYER2WIN] = universes[PLAYER2WIN]
    # For each game state in the current set of universes
    #   For each possible triple roll sum (3,4,...,9)
    #     Compute the next game state and increment the number of universes
    for game_state in universes:
        if (game_state == PLAYER1WIN) or (game_state == PLAYER2WIN):
            continue
        for roll3x in tdd:
            game_state_new = take_turn(game_state, roll3x)
            universes_next[game_state_new] += universes[game_state] * tdd[roll3x]
    return universes_next


def is_converged(universes):
    """All states are finished, i.e., one of the players has won."""
    return sorted(universes.keys()) == sorted([PLAYER1WIN, PLAYER2WIN])


##############################################################################

p1_start, p2_start = get_input()
print("Player 1 start:", p1_start)
print("Player 2 start:", p2_start)

# Play all games nondeterministically (i.e., nondeterministic turing machine)
universes = initialize_universes(p1_start, p2_start)
depth = 0
converged = False
while not converged:
    universes = advance_universes(universes)
    depth += 1
    print("At depth %d: %d game states, %d player1win, %d player2win" % \
        (depth,
        len(universes),
        universes.get(PLAYER1WIN, 0),
        universes.get(PLAYER2WIN, 0)))
    converged = is_converged(universes)

# Winner
if universes[PLAYER1WIN] > universes[PLAYER2WIN]:
    print("Player 1 wins in more universes:", universes[PLAYER1WIN])
elif universes[PLAYER2WIN] > universes[PLAYER1WIN]:
    print("Player 2 wins in more universes:", universes[PLAYER2WIN])
else:
    print("Players both win in equal number of universes:", universes[PLAYER1WIN])

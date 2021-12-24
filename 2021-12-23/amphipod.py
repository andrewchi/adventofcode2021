#!/usr/bin/env python3

import sys

def get_input():
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if (line == "#############") or (line == "#...........#"):
            continue
        elif line == "#########":
            continue
        elif line.startswith("###") and line.endswith("###"):
            first_room_row = line.strip("#").split("#")
        elif line.startswith("#") and line.endswith("#"):
            second_room_row = line.strip("#").split("#")
    return [first_room_row, second_room_row]


def initial_game_state(initial_rows):
    """
    Game state example. Upper left hallway space is (0, 2). x increases
    rightward and y increases upward.

    #############
    #.....D.D.A.#
    ###.#B#C#.###
      #A#B#C#.#
      #########

    With 5513 energy having been spent to get to this position.

    (("A1",2,0,"MOVABLE"), ("A2",9,2,"MOVABLE"),
     ("B1",4,0,"FINAL"), ("B2",4,1,"FINAL"),
     ("C1",6,0,"MOVABLE"), ("C2",6,1,"FINAL"),
     ("D1",5,2,"MOVABLE"), ("D2",7,2,"MOVABLE"),
     5513)
    """
    letters_seen = set()
    game_state = []
    for i in range(len(initial_rows)):
        row = initial_rows[i]
        for j in range(len(row)):
            letter = row[j]
            if letter in letters_seen:
                num_str = "2"
            else:
                num_str = "1"
                letters_seen.add(letter)
            amphipod = letter + num_str  # example: "A2"
            x = 2 * (j+1)
            y = 1 - i
            game_state.append((amphipod,x,y,"MOVABLE"))
    game_state = sorted(game_state)
    energy_spent = 0
    game_state.append(energy_spent)
    return tuple(game_state)


#############################################################################

initial_rows = get_input()
print("Initial positions (rows):", initial_rows)
gs = initial_game_state(initial_rows)
print("Initial game state:", gs)

#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np

def read_inputs():
    """Returns (1) list of random numbers, (2) list of numpy bingo boards"""
    first_line = True
    partial_matrix = []
    random_numbers = []
    bingo_boards = []
    for line in sys.stdin:
        if first_line:
            if line.strip() == "":
                continue
            random_numbers = [int(x) for x in line.split(",")]
            first_line = False
        else:
            if line.strip() != "":  # collect a row of the matrix
                row = [int(x) for x in line.split()]
                partial_matrix.append(row)
            else:                   # all done with this matrix
                if len(partial_matrix) == 0:
                    continue
                b = np.array(partial_matrix, dtype=int)
                bingo_boards.append(b)
                partial_matrix = []
    if len(partial_matrix) != 0:
        b = np.array(partial_matrix, dtype=int)
        bingo_boards.append(b)
        partial_matrix = []
    return random_numbers, bingo_boards

def is_winner(chip_board):
    rows, cols = chip_board.shape
    row_win = np.any(np.all(chip_board, axis=0))
    col_win = np.any(np.all(chip_board, axis=1))
    return row_win or col_win

def mark_all_hits(n, bingo_boards, chip_boards):
    return [c | (b == n) for b, c in zip(bingo_boards, chip_boards)]

def winning_score(bingo_board, chip_board):
    assert is_winner(chip_board)
    return np.sum(bingo_board * (~chip_board).astype(int))

def print_state(chip_boards, bingo_boards):
    for b, c in zip(bingo_boards, chip_boards):
        print("\n", b, "\n", c)

# Get inputs
random_numbers, bingo_boards = read_inputs()
chip_boards = [np.zeros(b.shape, dtype=bool) for b in bingo_boards]

# Run through random numbers, stopping at the first winner
winner_found = False
winner_score = 0
for n in random_numbers:
    chip_boards = mark_all_hits(n, bingo_boards, chip_boards)
    for b, c in zip(bingo_boards, chip_boards):
        if is_winner(c):
            winner_found = True
            winner_score = winning_score(b, c)
            print("Winner:\n", b, "\n", c)
    if winner_found:
        break
print("Final number:", n)
print("Winning board score:", winner_score)
print("Number * board score:", n * winner_score)

#!/usr/bin/env python3

import sys


def get_input():
    lines = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        lines.append(line)
    return lines


PAREN_SIBLING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
    ")": "(",
    "]": "[",
    "}": "{",
    ">": "<"
}


ERROR_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137
}


def check_paren(s):
    pstack = []   # parentheses stack
    for c in s:
        if c in '([{<':
            pstack.append(c)
        else:
            if (len(pstack) > 0) and (pstack[-1] == PAREN_SIBLING[c]):
                pstack.pop()
            else:
                return c
    return len(pstack) == 0


all_lines = get_input()

total_points = 0
for line in all_lines:
    check = check_paren(line)
    if check in ERROR_POINTS:
        points = ERROR_POINTS[check]
    else:
        points = 0
    total_points += points
    print(line, ":::", check, points)
print("Total points:", total_points)

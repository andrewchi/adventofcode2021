#!/usr/bin/env python3

import sys
import numpy as np

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


def check_paren(s):
    pstack = []   # parentheses stack
    for c in s:
        if c in '([{<':
            pstack.append(c)
        else:
            if (len(pstack) > 0) and (pstack[-1] == PAREN_SIBLING[c]):
                pstack.pop()
            else:
                return c     # syntax error on this character
    return len(pstack) == 0  # True if complete, False if incomplete


def complete_paren(s):
    assert(check_paren(s) == False)
    pstack = []   # parentheses stack
    for c in s:
        if c in '([{<':
            pstack.append(c)
        else:
            assert((len(pstack) > 0) and (pstack[-1] == PAREN_SIBLING[c]))
            pstack.pop()
    # complete all the rest
    completion = []
    while len(pstack) > 0:
        completion.append(PAREN_SIBLING[pstack.pop()])
    return "".join(completion)


def score_completion(s):
    COMPLETION_POINTS = {
        ")": 1,
        "]": 2,
        "}": 3,
        ">": 4
    }
    point_total = 0
    for c in s:
        point_total *= 5
        point_total += COMPLETION_POINTS[c]
    return point_total


###########################################################################

all_lines = get_input()

completions = [complete_paren(s) for s in all_lines if check_paren(s) == False]
scores = [score_completion(s) for s in completions]
for c, s in zip(completions, scores):
    print(c, s)
print("Median score:", int(np.median(scores)))

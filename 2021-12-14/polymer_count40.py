#!/usr/bin/env python3

import sys
import collections

def get_input():
    template = None
    rules = {}
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if "->" in line:
            fields = line.split()
            rules[fields[0]] = fields[2]
        else:
            template = line
    return template, rules


def string2pairs(s):
    pairs = collections.defaultdict(int)
    for i in range(len(s)-1):
        pairs[s[i:i+2]] += 1
    return pairs


def polymerize_step(pairs, rules):
    new_pairs = collections.defaultdict(int)
    for p in pairs:
        if p not in rules:
            continue
        middle_elt = rules[p]
        new_pairs[p[0] + middle_elt] += pairs[p]
        new_pairs[middle_elt + p[1]] += pairs[p]
    return new_pairs


def elt_count(template, pairs):
    """Compute the numbers of each element.  Each member of a pair has been
    counted twice, except for the first and last element of the template."""
    elt_hist_x2 = collections.defaultdict(int)
    first = template[0]
    last = template[-1]
    elt_hist_x2[first] += 1
    elt_hist_x2[last] += 1
    for p in pairs:
        elt_hist_x2[p[0]] += pairs[p]
        elt_hist_x2[p[1]] += pairs[p]
    elt_hist = {}
    for e in elt_hist_x2:
        elt_hist[e] = int(elt_hist_x2[e] / 2)
    return elt_hist


###########################################################################
template, rules = get_input()
print(template)
print(rules)

# Create initial pair counts
pairs = string2pairs(template)

# Run some polymerization steps
for i in range(40):
    pairs = polymerize_step(pairs, rules)
    print("Pair counts after step %d:" % (i+1), pairs)

# Count elements
elt_hist = elt_count(template, pairs)
print("Element counts after step %d:" % (i+1), elt_hist)
print("Max - min:", max(elt_hist.values()) - min(elt_hist.values()))

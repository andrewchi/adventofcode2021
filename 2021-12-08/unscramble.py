#!/home/andrew/.envs/venv38/bin/python3

import sys
import itertools

def get_input():
    displays = []
    for line in sys.stdin:
        fields = line.strip().split()
        assert(len(fields) == 10 + 1 + 4)
        ten_digits = [x for x in fields[:10]]
        assert(len(ten_digits) == 10)
        output_value = [x for x in fields[11:]]
        assert(len(output_value) == 4)
        ssdisplay = {}
        ssdisplay["ten_digits"] = ten_digits
        ssdisplay["output_value"] = output_value
        displays.append(ssdisplay)
    return displays

# Digit    Segments  (on a normal working display)
# -----    --------
# 0        6 - abcefg
# 1        2 - cf
# 2        5 - acdeg
# 3        5 - acdfg
# 4        4 - bcdf
# 5        5 - abdfg
# 6        6 - abdefg
# 7        3 - acf
# 8        7 - abcdefg
# 9        6 - abcdfg

NORMAL_WIRING_CODE = {
    "abcefg":  0,
    "cf":      1,
    "acdeg":   2,
    "acdfg":   3,
    "bcdf":    4,
    "abdfg":   5,
    "abdefg":  6,
    "acf":     7,
    "abcdefg": 8,
    "abcdfg":  9
}

def permute_wiring(s, ss_perm=None):
    if ss_perm is None:
        rewired_s = s
    else:
        rewired_s = [ss_perm[ord(c) - ord('a')] for c in s]
    sorted_rewired_s = "".join(sorted(rewired_s))
    return sorted_rewired_s

def is_legal_permutation(ten_wirings, ss_perm):
    # Check if the given permutation creates:
    #   1. A legal decoding
    #   2. Covers all 10 digits
    digits_covered = set()
    for s in ten_wirings:
        rewired_s = permute_wiring(s, ss_perm)
        if rewired_s in NORMAL_WIRING_CODE:
            digits_covered.add(NORMAL_WIRING_CODE[rewired_s])
        else:
            return False
    if len(digits_covered) == 10:
        return True
    else:
        return False

def decode_display(d):
    ten_wirings = d["ten_digits"]
    output_value = d["output_value"]
    # Try all permutations to see if there is a legal one
    SS_PERMUTATIONS = itertools.permutations("abcdefg")
    correct_perm = None
    for ss_perm in SS_PERMUTATIONS:
        if is_legal_permutation(ten_wirings, ss_perm):
            correct_perm = ss_perm
            break
    assert(correct_perm is not None)
    #print("Found correct permutation:", correct_perm)
    # Apply the correct permutation
    permuted_wirings = [permute_wiring(w, correct_perm) for w in output_value]
    out_digits = [NORMAL_WIRING_CODE[pw] for pw in permuted_wirings]
    return int("".join(str(x) for x in out_digits))

# Unscramble each line and get output
ssdisplays = get_input()
all_outputs = []
for ssd in ssdisplays:
    #print(ssd)
    out = decode_display(ssd)
    print("Decoded output", " ".join(ssd["output_value"]), "=", out)
    all_outputs.append(out)
print("Sum of all output values:", sum(all_outputs))

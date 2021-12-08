#!/home/andrew/.envs/venv38/bin/python3

import sys

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

# Count number of easy digits in output values (1, 4, 7 8)
# Lengths of easy digits: 2, 4, 3, 7
ssdisplays = get_input()
# print(ssdisplays)
n_easy_digits = 0
easy_digit_lengths = set([2,4,3,7])
for ssd in ssdisplays:
    for d in ssd["output_value"]:
        if len(d) in easy_digit_lengths:
            n_easy_digits += 1
print("Number of easy digits:", n_easy_digits)

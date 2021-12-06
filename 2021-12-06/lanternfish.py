#!/home/andrew/.envs/venv38/bin/python3

import sys

def read_input():
    whole_file = sys.stdin.read()
    timers = [int(x) for x in whole_file.strip().split(",")]
    return timers

def age_one_day(timers):
    next_timers = []
    new_lanternfish = []
    for t in timers:
        if t > 0:
            next_timers.append(t-1)
        else:
            next_timers.append(6)
            new_lanternfish.append(8)
    next_timers.extend(new_lanternfish)
    return next_timers

timers = read_input()
numdays = 80
for i in range(numdays):
    timers = age_one_day(timers)
print("Number of lanternfish after %d days: %d" % (numdays, len(timers)))
#print("Lanternfish timers:", timers)

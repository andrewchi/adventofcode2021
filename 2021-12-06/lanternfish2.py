#!/home/andrew/.envs/venv38/bin/python3

import sys
import collections

# Instead of keeping every lanternfish, record the number of lanternfish
# that have each timer value.

def read_input():
    whole_file = sys.stdin.read()
    timers = [int(x) for x in whole_file.strip().split(",")]
    timer_hist = collections.defaultdict(int)
    for t in timers:
        timer_hist[t] += 1
    return timer_hist

def age_one_day(timer_hist):
    next_timer_hist = collections.defaultdict(int)
    for t in timer_hist:
        if t > 0:
            next_timer_hist[t-1] += timer_hist[t]
        else:
            next_timer_hist[6] += timer_hist[0]
            next_timer_hist[8] += timer_hist[0]
    return next_timer_hist

timer_hist = read_input()
numdays = 256
for i in range(numdays):
    timer_hist = age_one_day(timer_hist)
print("Number of days:", numdays)
print("Lanternfish timers histogram:")
for t in timer_hist:
    print(t, ":", timer_hist[t])
print("Number of lanternfish:", sum(timer_hist.values()))

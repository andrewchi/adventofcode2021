#!/home/andrew/.envs/venv38/bin/python3

import sys
import numpy as np

def get_input():
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        if line.startswith("target area:"):
            fields = line.split()
            x_region = tuple(int(x) for x in fields[2].strip("x=,").split(".."))
            y_region = tuple(int(y) for y in fields[3].strip("y=,").split(".."))
            target = {"x":x_region, "y":y_region}
            return target


def trial_range(target):
    """Estimate a trial range of velocities."""
    assert min(target["x"]) > 0
    assert max(target["y"]) < 0
    min_vy = min(target["y"])
    max_vy = -min(target["y"])
    min_vx = 1
    max_vx = max(target["x"])
    vrange = {"x":(min_vx, max_vx), "y":(min_vy, max_vy)}
    return vrange


def fire(v0, target):
    """Returns an array of coordinates that the probe would follow if it was
    launched from (0,0) with initial velocity v0.  Stop when the probe is
    clearly below the target region and has negative y-velocity.

    Example: v0 = {"x":10, "y":-2}
    """
    assert v0["x"] >= 0
    n_points = 5
    beyond_the_target = False
    points = None
    while not beyond_the_target:
        n_points *= 2
        velocities_y = np.arange(v0["y"], v0["y"] - n_points, -1, dtype=int)
        positions_y = np.cumsum(velocities_y)
        if (positions_y[-1] < min(target["y"])) and (velocities_y[-1] < 0):
            beyond_the_target = True
        velocities_x = np.arange(v0["x"], v0["x"] - n_points, -1, dtype=int)
        velocities_x = np.maximum(0, velocities_x)
        positions_x = np.cumsum(velocities_x)
        points = np.transpose(np.array([positions_x, positions_y]))
    return points


def is_hit(points, target):
    """For each point [x,y] in the 2D numpy array of points, indicate True
    if the point is within the target region.
    """
    x_hit = (points[:,0] >= target["x"][0]) & (points[:,0] <= target["x"][1])
    y_hit = (points[:,1] >= target["y"][0]) & (points[:,1] <= target["y"][1])
    return x_hit & y_hit


##########################################################################

target = get_input()
print("Target region:", target)

vrange = trial_range(target)
print("Trial velocity ranges:", vrange)

max_y = 0  # maximum y of any trajectory that hits the target area
num_velocities_that_hit = 0
for vx in range(vrange["x"][0], vrange["x"][1]+1):
    for vy in range(vrange["y"][0], vrange["y"][1]+1):
        v0 = {"x":vx, "y":vy}
        points = fire(v0, target)
        any_hits = np.any(is_hit(points, target))
        if any_hits:
            max_y = max(max_y, np.max(points[:,1]))
            num_velocities_that_hit += 1
            print("v0=%s" % str(v0),
                "hit=%s" % str(any_hits),
                "max_y=%d" % np.max(points[:,1]))
print("Maximum y of any trajectory that hits the target area:", max_y)
print("Number of velocities that hit the target area:", num_velocities_that_hit)

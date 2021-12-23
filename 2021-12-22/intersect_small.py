#!/home/andrew/.envs/venv38/bin/python3

import sys

import numpy as np

def get_input():
    cuboids = []
    for line in sys.stdin:
        line = line.strip()
        if len(line) == 0:
            continue
        fields = line.split()
        cuboid = {}
        cuboid["mode"] = fields[0]
        for dim_region in fields[1].split(","):
            axis = dim_region.split("=")[0]
            lower_bound = int(dim_region.split("=")[1].split("..")[0])
            upper_bound = int(dim_region.split("=")[1].split("..")[1])
            assert lower_bound <= upper_bound
            cuboid[axis] = (lower_bound, upper_bound)
        cuboids.append(cuboid)
    return cuboids


def cuboid_to_bbox(cuboid):
    """Change notation from closed intervals to the half open intervals that are
    typically used in python/numpy indexing.  This enables us to think of the
    numbers as 3D bounding boxes (wireframe line segments enclosing a volume).

    Example:

       on x=-20..26,y=-36..17,z=-47..7

    becomes

      on x=[-20, 27), y=[-36, 18), z=[-47, 8)
    """
    bbox = {}
    bbox["mode"] = cuboid["mode"]
    bbox["x"] = (cuboid["x"][0], cuboid["x"][1] + 1)
    bbox["y"] = (cuboid["y"][0], cuboid["y"][1] + 1)
    bbox["z"] = (cuboid["z"][0], cuboid["z"][1] + 1)
    return bbox


class BoundingGrid(object):
    """Union of all bounding planes of the form x=*, y=*, and z=*.

    Also provide functions to convert between bounding planes and cuboids
    (slice_indices) of a hypothetical bit matrix, such that each cell represents
    an individual bounding box being on or off.
    """
    def __init__(self, bboxes):
        self.bounding_planes = {}
        for axis in ["x", "y", "z"]:
            bounds_min = set(b[axis][0] for b in bboxes)
            bounds_max = set(b[axis][1] for b in bboxes)
            self.bounding_planes[axis] = sorted(bounds_min | bounds_max)
        self.slice_indices = {"x":{}, "y":{}, "z":{}}
        for axis in ["x", "y", "z"]:
            for i in range(len(self.bounding_planes[axis])):
                bound = self.bounding_planes[axis][i]
                self.slice_indices[axis][bound] = i

    def __str__(self):
        return "Bounding planes: " + str(self.bounding_planes)

    def slice_index(self, axis, bound):
        return self.slice_indices[axis][bound]

    def bound(self, axis, slice_index):
        return self.bounding_planes[axis][slice_index]

    def cell_lengths(self):
        cl = {}
        cl["x"] = np.ediff1d(self.bounding_planes["x"])
        cl["y"] = np.ediff1d(self.bounding_planes["y"])
        cl["z"] = np.ediff1d(self.bounding_planes["z"])
        return cl

    def bitmatrix_shape(self):
        s = tuple(len(self.bounding_planes[axis]) - 1 for axis in ["x","y","z"])
        return s

    #def areas_yz(self):
    #    dy = np.ediff1d(self.bounding_planes["y"])
    #    dz = np.ediff1d(self.bounding_planes["z"])
    #    return np.outer(dy, dz)


def run_bboxes(bboxes):
    """Apply the on/off instructions to the bounding boxes, compressed as
    a bit matrix representing indivisible bounding boxes in the entire region.
    """
    bg = BoundingGrid(bboxes)
    bm = np.zeros(bg.bitmatrix_shape(), dtype=bool)
    for b in bboxes:
        x0 = bg.slice_index("x", b["x"][0])
        x1 = bg.slice_index("x", b["x"][1])
        y0 = bg.slice_index("y", b["y"][0])
        y1 = bg.slice_index("y", b["y"][1])
        z0 = bg.slice_index("z", b["z"][0])
        z1 = bg.slice_index("z", b["z"][1])
        if b["mode"] == "on":
            value = True
        else:
            value = False
        print("Applying bbox:", b)
        bm[x0:x1, y0:y1, z0:z1] = value
    # Compute volume (in original bounding box space) that is "on"
    cell_lengths = bg.cell_lengths()
    areas_yz = np.outer(cell_lengths["y"], cell_lengths["z"])
    on_volume = 0
    for i in range(bm.shape[0]):
        assert bm[i].shape == areas_yz.shape
        on_volume += cell_lengths["x"][i] * np.sum(bm[i] * areas_yz)
    return bm, bg, on_volume


def run_bboxes_simple(bboxes):
    x_min = min(b["x"][0] for b in bboxes)
    x_max = max(b["x"][1] for b in bboxes)
    y_min = min(b["y"][0] for b in bboxes)
    y_max = max(b["y"][1] for b in bboxes)
    z_min = min(b["z"][0] for b in bboxes)
    z_max = max(b["z"][1] for b in bboxes)
    simple_shape = (x_max-x_min, y_max-y_min, z_max-z_min)
    simple_bm = np.zeros(simple_shape, dtype=bool)
    for b in bboxes:
        if b["mode"] == "on":
            value = True
        else:
            value = False
        x0, x1 = b["x"][0] - x_min, b["x"][1] - x_min
        y0, y1 = b["y"][0] - y_min, b["y"][1] - y_min
        z0, z1 = b["z"][0] - z_min, b["z"][1] - z_min
        simple_bm[x0:x1, y0:y1, z0:z1] = value
    return simple_bm, np.sum(simple_bm)



def is_small(cuboid):
    if (cuboid["x"][0] < -50) or (cuboid["x"][1] > 50):
        return False
    if (cuboid["y"][0] < -50) or (cuboid["y"][1] > 50):
        return False
    if (cuboid["z"][0] < -50) or (cuboid["z"][1] > 50):
        return False
    return True


############################################################################

cuboids = get_input()
#print("cuboids:", cuboids)
bboxes = [cuboid_to_bbox(c) for c in cuboids if is_small(c)]
print("bboxes: ", bboxes)
bg = BoundingGrid(bboxes)
print(bg)
print("Cell lengths:", bg.cell_lengths())

print("Bitmatrix shape:", bg.bitmatrix_shape())
bm, _, on_volume = run_bboxes(bboxes)
#print("Bitmatrix:", bm.astype(int))
print("Volume of 'on' cells:", on_volume)
bm_simple, on_volume_simple = run_bboxes_simple(bboxes)
#print("Bitmatrix (simple method):", bm_simple.astype(int))
print("Volume of 'on' cells (simple method):", on_volume_simple)

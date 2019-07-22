import numpy
import re

from collections import Counter

filename = "input.txt"
#filename = "jonathan_paulson.txt"

import time
start_time = time.time()


def taxicab(a, b):
    """taxicab metric"""
    return sum(abs(a1 - b1) for a1, b1 in zip(a, b))


class Octahedron:
    conversion_matrix = numpy.array([
        [-1, 1, 1],
        [1, -1, 1],
        [1, 1, -1],
        [-1, -1, -1]
    ], dtype=int)

    def __init__(self, center, radius):
        self.center = numpy.array(center, dtype=int)
        self.radius = radius
        self.compute_bounding_box()

    def compute_bounding_box(self):
        box = self.radius * (numpy.zeros((4, 2), dtype=int) + [-1, 1])
        offset = self.conversion_matrix @ self.center
        self.box = box + offset[:, None]
        self.bounding_box = BoundingBox(self.box)

class BoundingBox:
    def __init__(self, box):
        self.box = numpy.array(box, dtype=int)

    def dist_from_origin(self):
        optimal = float('inf')
        for i in range(2): # need all odd, or all even case
            box = self.box - (0, 1)
            box += (i - box) % 2
            bb = BoundingBox(box)
            bb.minimize_bounds() # Does not change parity
            box = bb.box
            if not bb.is_empty():
                lower_bound = 0
                lower_bound = max(lower_bound, numpy.max(box[:, 0]))
                lower_bound = max(lower_bound, numpy.max(-box[:, 1]))
                optimal = min(optimal, lower_bound)
        return optimal

    def minimize_bounds(self):
        # To minimize the bounds [a1, b1], ..., [a4, b4] we do
        # a_1 -> max(a_1, -b_2-b_3-b_4)
        # b_1 -> min(b_1, -a_2-a_3-a_4) etc

        box = self.box
        bound_limits = box - numpy.sum(box, 0)
        box[:, 0] = numpy.maximum(box[:, 0], bound_limits[:, 1])
        box[:, 1] = numpy.minimum(box[:, 1], bound_limits[:, 0])

    def is_empty(self):
        for i in range(2):
            box = self.box - (0, 1)
            box += (i - box) % 2
            sums = numpy.sum(self.box, 0)
            if (sums[0] <= 0) and (sums[1] >= 0) and numpy.all(self.box[:, 0] <= self.box[:, 1]):
                return False
        return True

    def __repr__(self):
        return "<BoundingBox: {}>".format(self.box)

class Solver:
    def __init__(self, rectangles):
        self.rectangles = rectangles
        self.n = len(rectangles)
        self.dimension = len(rectangles[0].box)
        for r in rectangles:
            assert len(r.box) == self.dimension

    def solve(self):
        self.max_found = 0
        self.max_regions = []
        self.scan_axes()
        return self.max_regions

    def scan_axes(self, bounds=(), octants=None):
        rects = octants or self.rectangles
        axis = len(bounds)
        pruned_rects = []
        # bounds contains a list of ranges (a1, b1), (a2, b2),... which indicate
        # where we are scanning. we will only keep bounding boxes that intersect
        # with these bounds
        for r in rects:
            restricted = r.box.copy()
            # we check if there is at least one integer point where all terms
            # are even, or all odd. if so, add it to pruned_rects
            for j, (lb, ub) in enumerate(bounds):
                restricted[j, 0] = max(restricted[j, 0], lb)
                restricted[j, 1] = min(restricted[j, 1], ub)
            for parity in range(2):
                temp_box = restricted - (0, 1)
                temp_box += (parity - temp_box)%2
                summed = numpy.sum(temp_box, 0)
                if numpy.all(temp_box[:, 0] <= temp_box[:, 1]) and (summed[0] <= 0 <= summed[1]):
                    pruned_rects.append(r)
                    break

        rects = pruned_rects

        lowers = [r.box[axis, 0] for r in rects]
        after_uppers = [r.box[axis, 1] + 1 for r in rects]

        lower_counts = Counter(lowers)
        after_upper_counts = Counter(after_uppers)
        all_events = sorted(set(lowers + after_uppers))
        value = 0
        last_change = None

        max_in_sweep = 0
        chunks_with_vals = []
        for evt in all_events:
            change = lower_counts[evt] - after_upper_counts[evt]
            if last_change is not None:
                chunks_with_vals.append((value, (last_change, evt-1)))
            value += change
            last_change = evt
        chunks_with_vals.sort(reverse=True)

        for count, (lb, ub) in chunks_with_vals:
            if count < self.max_found:
                continue # no point continuing as over estimate is below the best we have so far
            if axis + 1 < self.dimension:
                if count >= self.max_found: # The value is already an over estimate, so we skip if there is no chance of improving our best so far
                    self.scan_axes(bounds + ((lb, ub),), rects)
            else:
                if count > self.max_found:
                    print("New max found!", count)
                    self.max_found = count
                    self.max_regions[:] = []
                if count == self.max_found:
                    self.max_regions.append((BoundingBox(bounds + ((lb, ub),)), count))

with open(filename) as f:
    lines = f.read().strip().splitlines()

def parse_line(line):
    p0, p1, p2, r = map(int, re.findall('-?\d+', line))
    return (p0, p1, p2), r

nanobots = [parse_line(l) for l in lines]

def dists_from(nanobot, nanobots):
    pos, r = nanobot
    dists = [taxicab(pos, nb[0]) for nb in nanobots]
    return dists

if __name__ == "__main__":
    print("Part 1")

    max_r = max(nanobots, key=lambda x: x[1])
    dists = dists_from(max_r, nanobots)
    print(sum(d <= max_r[1] for d in dists))

    octahedra = [Octahedron(bot[0], bot[1]).bounding_box for bot in nanobots]
    solver = Solver(octahedra)
    summaries = solver.solve()
    print("{} regions found".format(len(summaries)))
    max_overlaps = max(summaries, key=lambda x:x[1])[1]
    print("Max overlap count:", max_overlaps)

    least_dist = float('inf')
    for bounds in summaries:
        bb = bounds[0]
        dist = bb.dist_from_origin()
        least_dist = min(dist, least_dist)

    print("Least distance from origin:", least_dist)
    print("Elapsed: {:.2f}s".format(time.time() - start_time))


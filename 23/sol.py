import numpy
import re
import time

from argparse import ArgumentParser
from collections import Counter
from puztools import ints_from_lines, taxicab

def parse_line(item):
    return {'centre': item[:3], 'radius': item[3]}

def load(fn):
    with open(fn) as f:
        data = ints_from_lines(f.read())
    return [parse_line(item) for item in data]

def part_1(nanobots):
    max_radius = max(nanobots, key=lambda x: x['radius'])['radius']
    matching_nanobots = [bot for bot in nanobots if bot['radius'] == max_radius]
    assert len(matching_nanobots) == 1
    max_bot = matching_nanobots[0]
    count = sum(taxicab(bot['centre'], max_bot['centre']) <= max_radius for bot in nanobots)
    return count

class Octant:
    conversion_matrix = numpy.array([
        [-1, 1, 1],
        [1, -1, 1],
        [1, 1, -1],
        [-1, -1, -1]
    ], dtype=int)
    def __init__(self, array):
        self.bounds = numpy.array(array)

    @classmethod
    def from_data(cls, nanobot):
        centre = nanobot['centre']
        radius = nanobot['radius']
        bounds = (cls.conversion_matrix @ centre)[None].T + (-radius, radius)
        return cls(bounds)

    def restrict_bounds(self, bounds):
        new_bounds = self.bounds.copy()
        for i, (lower_b, upper_b) in enumerate(bounds):
            new_bounds[i, 0] = max(new_bounds[i, 0], lower_b)
            new_bounds[i, 1] = min(new_bounds[i, 1], upper_b)
        return Octant(new_bounds)

    def is_empty(self):
        return all(self.is_array_empty(array) for array in self.parity_arrays())

    def is_array_empty(self, array):
        if numpy.all(array[:, 0] <= array[:, 1]):
            sums = numpy.sum(array, 0)
            if sums[0] <= 0 and sums[1] >= 0:
                return False
        return True

    def parity_arrays(self):
        for parity in range(2):
            new_bounds = self.bounds - (0, 1)
            new_bounds += (parity - new_bounds) % 2
            yield new_bounds

    def minimize_bounds(self):
        bounds = self.bounds
        reduced_bounds = self.bounds.copy()
        sums = numpy.sum(bounds, 0)
        reduced_bounds[0,:] = numpy.maximum(bounds[0,:], (bounds - sums)[1,:])
        reduced_bounds[1,:] = numpy.minimum(bounds[1,:], (bounds - sums)[0,:])
        self.bounds = reduced_bounds

    def dist_from_origin(self):
        dist = float('inf')
        for array in self.parity_arrays():
            octant = Octant(array)
            octant.minimize_bounds()
            if not self.is_array_empty(array):
                lower_bound = numpy.max(array * (1, -1))
                lower_bound = max(0, lower_bound)
                dist = min(lower_bound, dist)
        return dist

    def __repr__(self):
        return "<Octant: {}>".format(self.bounds)

class AxisScanner:
    def __init__(self, octants):
        self.octants = octants

    def solve(self):
        self.max_found = 0
        self.min_distance = float('inf')
        self.scan_axes(self.octants, ())
        return self.min_distance

    def scan_axes(self, octants, bounds):
        pruned = []
        for octant in octants:
            restricted = octant.restrict_bounds(bounds)
            if not restricted.is_empty():
                pruned.append(restricted)

        axis = len(bounds)
        lowers = [octant.bounds[axis, 0] for octant in pruned]
        after_uppers = [octant.bounds[axis, 1] + 1 for octant in pruned]
        lower_counts = Counter(lowers)
        after_upper_counts = Counter(after_uppers)
        events = list(set(lowers + after_uppers))
        events.sort()
        last_event = None
        count = 0
        regions = []
        for evt in events:
            if last_event is not None:
                regions.append((count, (last_event, evt-1)))
            count += lower_counts[evt] - after_upper_counts[evt]
            last_event = evt
        regions.sort(reverse=True)
        for count, axis_bounds in regions:
            new_bounds = bounds + (axis_bounds,)
            if count < self.max_found:
                return
            if axis == 3:
                if count >= self.max_found:
                    distance = Octant(new_bounds).dist_from_origin()
                    if count == self.max_found:
                        self.min_distance = min(self.min_distance, distance)
                    else:
                        self.min_distance = distance
                        self.max_found = count
            else:
                self.scan_axes(pruned, new_bounds)

def part_2(nanobots):
    octants = [Octant.from_data(bot) for bot in nanobots]
    scanner = AxisScanner(octants)
    return scanner.solve()

def main():
    parser = ArgumentParser()
    parser.add_argument('filename', type=str)
    args = parser.parse_args()
    start_time = time.time()
    nanobots = load(args.filename)
    print("Part 1:")
    print(part_1(nanobots))
    print("Part 2:")
    print(part_2(nanobots))
    elapsed = time.time() - start_time
    print("Elapsed: {:.2f}s".format(elapsed))

if __name__ == "__main__":
    main()


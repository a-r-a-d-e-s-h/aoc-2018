import re

from collections import Counter

def solve(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    raw_vals = [tuple(map(int, re.findall('-?\d+', line))) for line in lines]
    rectangles = []
    for rect in raw_vals:
        assert len(rect) %2 == 0
        axes = len(rect) // 2
        new_rect = ()
        for i in range(axes):
            new_rect = new_rect + ((rect[i*2: (i+1)*2]),)
        rectangles.append(new_rect)

    solver = Solver(rectangles)
    summaries = solver.solve()
    max_overlaps = max(summaries, key=lambda x: x[1])[1]
    max_rectangles = [s for s in summaries if s[1] == max_overlaps]
    print("Maximum overlap:", max_overlaps)
    print("Maximum regions:")
    for rect in max_rectangles:
        print(rect)
    print("{} regions considered.".format(len(summaries)))

class Solver:
    def __init__(self, rectangles):
        self.rectangles = rectangles
        self.n = len(rectangles)
        self.dimension = len(rectangles[0])
        for r in rectangles:
            assert len(r) == self.dimension

    def solve(self):
        self.max_found = 0
        self.max_regions = []
        self.scan_axes()
        return self.max_regions

    def scan_axes(self, bounds=()):
        rects = self.rectangles
        axis = len(bounds)
        pruned_rects = []
        for r in rects:
            for (lb, ub), (l, u) in zip(bounds, r):
                if (l > ub) or (u < lb):
                    break
            else:
                # if we are in the 4th dimension, we need to check that the region actully contains any points
                # This is octahedron specific
                if axis == 3:
                    min_int = float('inf')
                    max_int = float('-inf')
                    min_x, min_y, min_z = map(lambda x: x[0], r[:3])
                    max_x, max_y, max_z = map(lambda x: x[1], r[:3])
                    for i in range(2):
                        min_int_x = min_x + i
                        min_int_y = min_y + (min_y + min_int_x) % 2
                        min_int_z = min_z + (min_z - min_int_x) % 2
                        if all((min_int_x <= max_x, min_int_y <= max_y, min_int_z <= max_z)):
                            min_int = min(min_int_x + min_int_y + min_int_z, min_int)

                        max_int_x = max_x - i
                        max_int_y = max_y - (max_y - max_int_x) % 2
                        max_int_z = max_z - (max_z - max_int_x) % 2
                    if all((min_x <= max_int_x, min_y <= max_int_y, min_z <= max_int_z)):
                        max_int = max(max_int_x + max_int_y + max_int_z, max_int)
                    if min_int <= max_int:
                        pruned_rects.append(r)
                else:
                    pruned_rects.append(r)

        rects = pruned_rects

        lowers = [r[axis][0] for r in rects]
        after_uppers = [r[axis][1] + 1 for r in rects]

        lower_counts = Counter(lowers)
        after_upper_counts = Counter(after_uppers)
        all_events = sorted(set(lowers + after_uppers))
        value = 0
        last_change = None

        max_in_sweep = 0

        for evt in all_events:
            change = lower_counts[evt] - after_upper_counts[evt]
            if last_change is not None:
                if axis + 1 < self.dimension:
                    if value >= self.max_found: # The value is already an over estimate, so we skip if there is no chance of improving our best so far
                        self.scan_axes(bounds + ((last_change, evt - 1),))
                else:
                    if value > self.max_found:
                        self.max_found = value
                        self.max_regions[:] = []
                    if value == self.max_found:
                        self.max_regions.append((bounds + ((last_change, evt - 1),), value))
            value += change
            last_change = evt





def main():
    solve("cubes1.txt")

if __name__ == "__main__":
    main()


import re
from collections import Counter

def taxicab(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def closest_to(pos, coordinates):
    min_dist = float('inf')
    min_index = None
    for index, coord in enumerate(coordinates):
        dist = taxicab(coord, pos)
        if dist == min_dist:
            min_index = None
        if dist < min_dist:
            min_index = index
            min_dist = dist
    return min_index


def part_1(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    coordinates = [list(map(int, re.findall('-?\d+', l))) for l in lines]


    xs = [p[0] for p in coordinates]
    ys = [p[1] for p in coordinates]
    grid = {}
    for x in range(min(xs), max(xs)+1):
        for y in range(min(ys), max(ys)+1):
            grid[x, y] = closest_to((x, y), coordinates)
    indices_on_edge = set()
    for (x, y) in grid.keys():
        if x in (min(xs), max(xs)):
            indices_on_edge.add(grid[x,y])
        if y in (min(ys), max(ys)):
            indices_on_edge.add(grid[x,y])
    count = Counter(grid.values())
    for index in indices_on_edge:
        del(count[index])
    return max(count.values())

def part_2(filename, dist_bound):
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    coordinates = [list(map(int, re.findall('-?\d+', l))) for l in lines]


    xs = [p[0] for p in coordinates]
    ys = [p[1] for p in coordinates]
    grid = {}
    for x in range(min(xs), max(xs)+1):
        for y in range(min(ys), max(ys)+1):
            grid[x, y] = sum(taxicab((x, y), coord) for coord in coordinates)

    # check edges...
    min_on_edge = float('inf')
    for (x, y) in grid.keys():
        if x in (min(xs), max(xs)):
            min_on_edge = min(min_on_edge, grid[x,y])
        if y in (min(ys), max(ys)):
            min_on_edge = min(min_on_edge, grid[x,y])
    if min_on_edge < dist_bound:
        print("min_on_edge =", min_on_edge)
        raise NotImplementedError

    else:
        return sum(1 for item in grid.values() if item < dist_bound)
 




def solve():
    p1 = part_1('test.txt')
    assert p1 == 17
    print("Part 1")
    print(part_1('input.txt'))

    assert part_2('test.txt', 32) == 16
    print(part_2('input.txt', 10000))

if __name__ == "__main__":
    solve()

import numpy
import re
from collections import Counter

def pl(line):
    coord = tuple(map(int, re.findall('-?\d+', line)))
    assert len(coord) == 4
    return coord

def taxicab(a, b):
    def absdif(pair):
        x, y = pair
        return abs(x - y)
    return sum(map(absdif, zip(a, b)))

def connected_stars(coordinates, dist):
    num_stars = len(coordinates)
    grid = numpy.zeros((num_stars, num_stars), dtype=bool)
    for i in range(num_stars):
        for j in range(num_stars):
            if taxicab(coordinates[i], coordinates[j]) <= dist:
                grid[i,j] = 1
    return grid

def partitions(grid):
    num_stars = grid.shape[0]
    partition_numbers = numpy.zeros(num_stars, dtype=int)
    for i in range(num_stars):
        part_num = i+1
        star_near = partition_numbers[grid[i]]
        if numpy.all(star_near == 0):
            partition_numbers[grid[i]] = part_num
        else:
            min_part = numpy.min(star_near[star_near != 0])
            other_parts = numpy.unique(star_near[star_near != 0])
            partition_numbers[grid[i]] = min_part
            for part in other_parts:
                partition_numbers[partition_numbers == part] = min_part
    return Counter(partition_numbers)



def part_1(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    coords = [pl(l) for l in lines]
    grid = connected_stars(coords, 3)
    parts = partitions(grid)
    return len(parts)


if __name__ == "__main__":
    assert part_1('test.txt') == 2
    assert part_1('test2.txt') == 4
    assert part_1('test3.txt') == 3
    assert part_1('test4.txt') == 8
    print(part_1('input.txt'))

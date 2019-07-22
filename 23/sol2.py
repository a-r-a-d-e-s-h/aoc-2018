import numpy
import re
import time

from itertools import product

start_time = time.time()

filename = 'corelax.txt'

with open(filename) as f:
    lines = f.read().strip().splitlines()

def parse_line(line):
    p0, p1, p2, r = map(int, re.findall('-?\d+', line))
    return (p0, p1, p2), r

nanobots = [parse_line(l) for l in lines]

def taxicab(a, b):
    """taxicab metric"""
    ret = []
    for a1, b1 in zip(a, b):
        ret.append(abs(a1-b1))
    return sum(ret)

def dists_from(nanobot, nanobots):
    pos, r = nanobot
    dists = [taxicab(pos, nb[0]) for nb in nanobots]
    return dists

print("Part 1")

max_r = max(nanobots, key=lambda x: x[1])
dists = dists_from(max_r, nanobots)
print(sum(d <= max_r[1] for d in dists))

# The algorithm following works on the assumption, which after investigation is not
# true! that if a group of bots are pairwise overlapping, then there is a common overlap
# for all of them. This does not affect the answer in all example inputs I've tried.

num_bots = len(nanobots)

# We build a num_bots x num_bots matrix with overlap_grid[i,j] = 0 or 1 according as
# the nanobots n_i and n_j have overlapping ranges

overlap_grid = numpy.zeros((num_bots, num_bots), dtype=int)


for i,j in product(range(num_bots), repeat=2):
    bot1, bot2 = nanobots[i], nanobots[j]
    pos1, r1 = bot1
    pos2, r2 = bot2
    if taxicab(pos1, pos2) <= r1 + r2:
         overlap_grid[i,j] = 1 # if the pair overlap...

# The following recursive function takes 'indices' a boolean mask over all nanobots
# and it takes on good faith that it is only given a mask corresponding to a group
# of nanobots whose ranges all mutually overlap

def find_max_collections(overlap_grid, indices, index_prod=None, max_size=0, min_dist_from_0 = float('inf')):
    tot_indices = numpy.sum(indices)
    current_rows = overlap_grid[indices]
    if index_prod is None:
        index_prod = numpy.ones(indices.shape, dtype=bool)
    if tot_indices:
        max_index = numpy.max(indices.nonzero()[0])
    else:
        max_index = -1

    if tot_indices > max_size:
        max_size = tot_indices
        min_dist_from_0 = float('inf') # for the value for the part 2 answer

    if tot_indices == max_size: # we have a maximal group, so check distance from 0,0,0
        dist = 0
        for index in indices.nonzero()[0]:
            bot = nanobots[index]
            dist = max(taxicab(bot[0], (0,0,0)) - bot[1], dist)
        min_dist_from_0 = min(dist, min_dist_from_0)

    remaining = index_prod
    remaining[indices] = False
    remaining[0:max_index+1] = False
    if numpy.sum(remaining) + tot_indices < max_size:
        return max_size, min_dist_from_0
    last_index = None
    for index in remaining.nonzero()[0]:
        indices[index]=True
        max_size, min_dist_from_0 = find_max_collections(overlap_grid, indices, index_prod & overlap_grid[index], max_size, min_dist_from_0)
        indices[index]=False
    return max_size, min_dist_from_0

max_size, min_dist = (find_max_collections(overlap_grid, numpy.zeros(num_bots, dtype=bool)))
print("Part 2 ({} nanobots in largest group)".format(max_size))
print(min_dist)
print("Time elapsed: {:.2f}s".format(time.time() - start_time))


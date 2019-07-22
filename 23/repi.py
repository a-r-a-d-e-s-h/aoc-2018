#!/usr/bin/env python3

import re
import numpy as np

if __name__ == '__main__':
    positions, radii = [], []
    with open('input', 'r') as f:
        for line in f:
            *pos, r = [int(i) for i in re.findall(r'-?\d+', line)]
            positions.append(pos)
            radii.append(r)
    positions = np.asarray(positions)
    radii = np.asarray(radii)

    #part 1
    idx = np.argmax(radii)
    r = radii[idx]
    pos = positions[idx]

    best = []
    def in_range(x, r = None, cache = {}):
        if tuple(x) in cache:
            return cache[tuple(x)]
        if r is None:
            r = radii
        dist = np.sum(np.abs(positions - x), axis = 1)
        near = np.sum(dist <= r) + 1/max(np.sum(np.abs(x)), 1)
        if not best:
            best.append((x, near))
        if near > best[-1][1]:
            best.append((x, near))
        cache[tuple(x)] = near
        return near
    print(int(in_range(pos, r)))
    
    sorted(positions, key = in_range)

    def neighbour_search(x, r = 1):
        neighbours = np.asarray([(i,j,k)
            for i in range(-1,2) 
            for j in range(-1,2)
            for k in range(-1,2) if any((i,j,k))])
        p = 0
        while True:
            p += 1
            dists = np.sum(np.abs(positions - x), axis = 1)
            weighted = dists - radii
            weighted[weighted <= 0] = 0
            changes = []
            for n in neighbours:
                dists_n = np.sum(np.abs(positions - (x + r*n)), axis = 1)
                weighted_n = dists_n - radii
                weighted_n[weighted_n <= 0] = 0
                dw = weighted_n - weighted
                changes.append(np.sum(dw))
            if all(c >= 0 for c in changes):
                break
            x += neighbours[np.argmin(changes)]*r
            in_range(x)
        return x
    
    # initial coarse search
    for r in [100000,1000,10]:
        neighbour_search(best[-1][0], r = r)

    # ignore bots that are too far away from current optimal point to make a
    # difference
    idx = (np.sum(np.abs(positions - best[-1][0]), axis = 1) - radii) < 1000
    positions = positions[idx]
    radii = radii[idx]

    neighbour_search(best[-1][0], r = 1)

    print(int(np.sum(best[-1][0])))

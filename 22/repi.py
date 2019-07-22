#!/usr/bin/env python3

import re
import collections

if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        depth, = [int(i) for i in re.findall(r'\d+', f.readline())]
        target = tuple([int(i) for i in re.findall(r'\d+', f.readline())])

    def index(x, y, cache = {target:0}):
        if y == 0:
            cache[x, y] = x*16807
        if x == 0:
            cache[x, y] = y*48271
        if (x, y) in cache:
            return cache[(x, y)]
        return erosion(x-1, y)[0]*erosion(x, y-1)[0]

    def erosion(x, y, cache = {}):
        if (x, y) in cache:
            return cache[(x, y)]
        level = (index(x, y) + depth)%20183
        t = {0:'.',1:'=',2:'|'}[level%3]
        cache[x, y] = (level, t)
        return level, t

    def risk(x, y, cache = {}):
        if (x, y) in cache:
            return cache[(x, y)]
        _, t = erosion(x, y)
        cache[(x, y)] = {'.':0,'=':1,'|':2}[t]
        return cache[(x, y)]

    def risk_region(xi, yi, xf, yf):
        return sum(risk(x, y) for x in range(xi, xf + 1) for y in range(yi, yf + 1))

    print(risk_region(0, 0, target[0], target[1]))

    inf = float('inf')
    shortest = collections.defaultdict(lambda:{'torch':inf,'gear':inf,'neither':inf})
    shortest[(0,0)] = {'torch':0,'gear':7,'neither':inf}

    compatible = {'.':['torch','gear'],
            '=':['gear','neither'],
            '|':['torch','neither']}

    def neighbours(x, y):
        n = [(x + 1, y), (x - 1, y), (x, y - 1), (x, y + 1)]
        for xi, yi in n:
            if xi >= 0 and yi >= 0:
                yield xi, yi

    def change_gear(x, y):
        d = shortest[(x, y)]
        t = erosion(x, y)[1]
        ta, tb = sorted(compatible[t], key = lambda x : d[x])
        if d[ta] == inf:
            return
        d[tb] = min(d[tb], d[ta] + 7)

    def minimize(x, y):
        t = erosion(x, y)[1]
        for tool in compatible[t]:
            m = min(shortest[(xn, yn)][tool] for xn, yn in neighbours(x, y)) + 1
            shortest[(x, y)][tool] = min(shortest[(x, y)][tool], m)
        change_gear(x, y)
        
    search_buffer = 150 # might be larger to ensure shortest path found
    for y in range(target[1] + search_buffer):
        for x in range(target[0] + search_buffer):
            minimize(x, y)
            [minimize(xn, yn) for xn, yn in neighbours(x, y)]
    
    print(shortest[target]['torch'])



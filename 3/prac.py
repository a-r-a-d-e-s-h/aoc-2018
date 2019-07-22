with open('input.txt') as f:
    lines = f.read().strip().splitlines()
import re
def pc(c):
    return tuple(map(int, re.findall('\d+', c)))

claims = [pc(c) for c in lines]

import numpy

grid = numpy.zeros((1000,1000))

for eid, x, y, w, h in claims:
    grid[x:x+w,y:y+h] += 1

print(numpy.sum(grid > 1))

for eid, x,y,w,h in claims:
    if numpy.all(grid[x:x+w,y:y+h]==1):
        print(eid)

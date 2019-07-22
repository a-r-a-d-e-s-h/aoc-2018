import re

regex = re.compile("#([0-9]+) @ ([0-9]+),([0-9]+): ([0-9]+)x([0-9]+)")
def parse_claim(claim):
    match = regex.match(claim).groups()
    claim_id, x, y, width, height = [int(x) for x in match]
    return {'id': claim_id, 'pos': (x,y), 'shape': (width,height)}


test_input = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""

real_input = open('input.txt').read()
claims = [parse_claim(x) for x in real_input.split('\n') if x]

import numpy

def p1(claims):
    grid = numpy.zeros((1000, 1000))
    for claim in claims:
        x,y = claim['pos']
        w,h = claim['shape']
        grid[y:y+h,x:x+w] += 1
    return numpy.sum(grid>1)


print(p1(claims))

def p2(claims):
    grid = numpy.zeros((1000, 1000))
    for claim in claims:
        x,y = claim['pos']
        w,h = claim['shape']
        grid[y:y+h,x:x+w] += 1
    for claim in claims:
        x,y = claim['pos']
        w,h = claim['shape']
        if numpy.all(grid[y:y+h,x:x+w] == 1):
            return claim['id']

print(p2(claims))



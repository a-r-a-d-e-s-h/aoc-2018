import time
start_time = time.time()

filename = 'input.txt'
with open(filename) as f:
    lines = f.read().strip().splitlines()

class Region:
    def __init__(self, x, y):
        coord = (x, y)

class Problem:
    modulo = 20183
    def __init__(self, depth, target):
        self.depth = depth
        self.target = target
        self.pre_computed = {}

    def geologic_index(self, x, y):
        if (x, y) not in self.pre_computed:
            self.pre_computed[x, y] = self.compute_geologic_index(x, y)
        return self.pre_computed[x, y]

    def compute_geologic_index(self, x, y):
        if (x, y) == (0, 0):
            return 0
        if (x, y) == self.target:
            return 0
        if y == 0:
            return x * 16807
        if x == 0:
            return y * 48271
        return  self.erosion_level(x-1, y) * self.erosion_level(x, y-1)

    def erosion_level(self, x, y):
        return (self.geologic_index(x, y) + self.depth)% Problem.modulo

    def type(self, x, y):
        return self.erosion_level(x, y) % 3

    def type_name(self, t):
        return ('rocky', 'wet', 'narrow')[t]
from itertools import product

print("Part 1")
depth = int(lines[0].split(': ')[1])
import re
target = tuple(map(int, re.findall('\d+', lines[1])))
prob = Problem(depth, target)
risk = sum(prob.type(x, y) for x, y in product(range(target[0]+1), range(target[1] + 1)))
print(risk)



terrains = ['rocky', 'wet', 'narrow']
tools = ['torch', 'climbing', 'neither']

infinity = float('inf')

def take_step(tool_dists):
    t, c, n = tool_dists
    rocky = [min(c+8, t+1), min(c+1, t+8), infinity]
    wet = [infinity, min(c+1, n+8), min(c+8, n+1)]
    narrow = [min(t+1, n+8), infinity,  min(t+8, n+1)]
    return (rocky, wet, narrow)

from collections import defaultdict
square_costs = defaultdict(lambda:[float('inf'), float('inf'), float('inf')])
square_costs[0, 0] = (0, 7, infinity)
optimals = set()
optimals.add((0, 0))


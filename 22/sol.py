import time
start_time = time.time()

filename = 'repiphany.txt'
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

print("Test")
prob = Problem(510, (10, 10))

grid = [[''] * 11 for __ in range(11)]
chars = ['.', '=', '|']

for x in range(11):
    for y in range(11):
        grid[y][x] = chars[prob.type(x, y)]

from itertools import product
risk = sum(prob.type(x, y) for x, y in product(range(11), repeat=2))
print(risk)

print("Part 1")
depth = int(lines[0].split(': ')[1])
import re
target = tuple(map(int, re.findall('\d+', lines[1])))
prob = Problem(depth, target)
risk = sum(prob.type(x, y) for x, y in product(range(target[0]+1), range(target[1] + 1)))
print(risk)

infinity = 1 << 20

torch = [[0]]
climbing = [[7]]
neither = [[infinity]]


def to_rocky(x, y):
    return [
        min(climbing[y][x]+7, torch[y][x])+1,
        min(climbing[y][x], torch[y][x]+7)+1,
        infinity
    ]

def to_wet(x, y):
    return [
        infinity,
        min(neither[y][x]+7, climbing[y][x])+1,
        min(neither[y][x], climbing[y][x]+7)+1
    ]

def to_narrow(x, y):
    return [
        min(torch[y][x], neither[y][x]+7)+1,
        infinity,
        min(torch[y][x]+7, neither[y][x])+1
    ]

def update_costs(start, dest):
    dest_type = prob.type(*dest)
    to_map = [to_rocky, to_wet, to_narrow]
    grids = [torch, climbing, neither]
    costs = to_map[dest_type](*start)
    current = [g[dest[1]][dest[0]] for g in grids]
    new_vals = list(min(xx, yy) for xx, yy in zip(current, costs))
    for grid, new_val in zip(grids, new_vals):
        grid[dest[1]][dest[0]] = new_val

def iterate_cost(direction):
    current_width = len(climbing[0])
    current_height = len(climbing)
    if direction == 'x':
        for grid in (torch, climbing, neither):
            for row in grid:
                row.append(infinity)
        new_x = current_width
        for y in range(current_height):
            update_costs((new_x - 1, y), (new_x, y))
    elif direction == 'y':
        for grid in (torch, climbing, neither):
            grid.append([infinity]*current_width)
        new_y = current_height
        for x in range(current_width):
            update_costs((x, new_y - 1), (x, new_y))
    can_minimize = True
    while can_minimize:
        can_minimize = False
        width = len(climbing[0])
        height = len(climbing)
        for row in range(height):
            for col in range(width):
                nbours = []
                if row > 0:
                    nbours.append((col, row-1))
                if col > 0:
                    nbours.append((col-1, row))
                if row+1 < height:
                    nbours.append((col, row+1))
                if col+1 < width:
                    nbours.append((col+1, row))
                for nbour in nbours:
                    old_vals = [g[nbour[1]][nbour[0]] for g in (torch, climbing, neither)]
                    update_costs(nbour, (col, row))
                    new_vals = [g[nbour[1]][nbour[0]] for g in (torch, climbing, neither)]
                    if new_vals != old_vals:
                        can_minimize = True

target_coord = prob.target

for i in range(target_coord[0]):
    iterate_cost('x')
for i in range(target_coord[1]):
    iterate_cost('y')
optimal = False
grids = [torch, climbing, neither]
while not optimal:
    width = len(torch[0])
    height = len(torch)
    min_costs = [[0]*width for __ in range(height)]
    for row in range(height):
        for col in range(width):
            min_costs[row][col] = min(g[row][col] for g in grids)
    target_cost = torch[target_coord[1]][target_coord[0]]
    min_last_col = min(row[-1] + abs(i - target_coord[1]) + width-1 - target_coord[0] for i, row in enumerate(min_costs))
    min_last_row = min(x + abs(i - target_coord[0]) + height-1 - target_coord[1] for i, x in enumerate(min_costs[-1]))
    if target_cost > min_last_col:
        iterate_cost('x')
        continue
    if target_cost > min_last_row:
        iterate_cost('y')
        continue
    optimal = True

print("Part 2")
print(torch[target_coord[1]][target_coord[0]])
print("Elapsed: {:.2f}s".format(time.time() - start_time))

import time
start = time.time()

filename = "input.txt"
with open(filename) as f:
    lines = f.read().strip().splitlines()

height = len(lines)
width = len(lines[0])

def nbours(row, col):
    min_row = max(row-1, 0)
    max_row = min(row+2, height)
    min_col = max(col-1, 0)
    max_col = min(col+2, width)
    def it():
        for r in range(min_row, max_row):
            for c in range(min_col, max_col):
                if r!= row or c != col:
                    yield (r, c)
    return list(it())

start_grid = [list(l) for l in lines]

from collections import Counter

def adj_counts(row, col, grid):
     chars = [grid[r][c] for (r,c) in nbours(row, col)]
     return Counter(chars)

def do_step(grid):
    height = len(grid)
    width = len(grid[0])

    new_grid = [[0]*width for __ in range(height)]

    for row in range(height):
        for col in range(height):
            char = grid[row][col]
            counts = adj_counts(row, col, grid)
            if char == '.':
                new_grid[row][col] = '|' if counts['|'] >= 3 else '.'
            elif char == '|':
                new_grid[row][col] = '#' if counts['#'] >= 3 else '|'
            elif char == '#':
                new_grid[row][col] = '#' if counts['#']*counts['|'] else '.'
    return new_grid

def compute_steps(grid, n):
    log = []
    grid_as_str = '\n'.join(''.join(l) for l in grid)
    log.append(grid_as_str) 
    for i in range(n):
        grid = do_step(grid)
        grid_as_str = '\n'.join(''.join(l) for l in grid)
        if grid_as_str in log:
            first_repeat = i+1
            break
        log.append(grid_as_str)
    else:
        return grid
    first_index = log.index(grid_as_str)
    period = first_repeat - first_index
    return log[first_index + (n - first_index)%period]

print("Part 1")

grid = compute_steps(start_grid, 10)
from itertools import chain

counts = Counter(chain(*grid))
print(counts['|'] * counts['#'])

print("Part 2")
grid = compute_steps(start_grid, 1000000000)
counts = Counter(chain(*grid))
print(counts['|'] * counts['#'])

print("Time elapsed: {:.2f}s".format(time.time() - start))

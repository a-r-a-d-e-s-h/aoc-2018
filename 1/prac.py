with open('input.txt') as f:
    lines = f.read().strip().splitlines()

vals = tuple(map(int, lines))

print(sum(vals))

visited = set()
cur_sum = 0

from itertools import cycle

for val in cycle(vals):
    if cur_sum in visited:
        print(cur_sum)
        break
    visited.add(cur_sum)
    cur_sum += val


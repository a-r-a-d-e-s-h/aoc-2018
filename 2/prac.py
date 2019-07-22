with open('input.txt') as f:
    lines = f.read().strip().splitlines()

from collections import Counter as C
x = sum(2 in C(l).values() for l in lines)
y = sum(3 in C(l).values() for l in lines)

print(x*y)

from itertools import combinations as combs

for x1,x2 in combs(lines, 2):
    common = ''.join(a1 for a1,a2 in zip(x1,x2) if a1==a2)
    if len(common) + 1 == len(x1):
        print(common)

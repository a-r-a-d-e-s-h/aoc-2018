from collections import deque
import re

def solve(filename, remove_chars = ''):
    with open(filename) as f:
        line = f.read().strip()
    if remove_chars:
        line = re.sub('[{}]'.format(remove_chars.lower() + remove_chars.upper()), '', line)
        
    return calc_reduced_len(line)

def calc_reduced_len(line):
    col = deque(line)
    length = len(col)
    all_ok = 0
    index = 0
    while 1:
        try:
            if col[index] != col[index+1] and col[index].lower() == col[index+1].lower():
                col.rotate(-index)
                col.popleft()
                col.popleft()
                col.rotate(index)
                index = max(0, index - 1)
                continue
        except IndexError:
            return len(col)
        index += 1


def part_1():
    assert solve('test.txt') == 10
    print("Part 1")
    print(solve('input.txt'))

def min_over_chars(filename):
    min_len = float('inf')
    for char in 'abcdefghijklmnopqrstuvwxyz':
        min_len = min(solve(filename, char), min_len)
    return min_len

def part_2():
    assert min_over_chars('test.txt') == 4
    print("Part 2")
    print(min_over_chars('input.txt'))

if __name__ == "__main__":
    part_1()
    part_2()

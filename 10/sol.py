with open('input.txt', 'r') as f:
    data = f.read()

import re

def parse_line(line):
    regex = re.compile("position=<\s*(-?[0-9]+),\s*(-?[0-9]+)> velocity=<\s*(-?[0-9]+),\s*(-?[0-9]+)>")    
    res = regex.match(line)
    if res:
        return [int(x) for x in res.groups()]

lines = data.split('\n')
lines = [l for l in lines if l]

class Point:
    def __init__(self, pos, vel):
        self.position = pos
        self.velocity = vel

    def steps(self, n):
        pos = self.position
        vel = self.velocity
        pos[0] += vel[0]*n
        pos[1] += vel[1]*n

    def pos_at(self, n):
        return [self.velocity[0]*n + self.position[0], self.velocity[1]*n + self.position[1]]

points = []

for line in lines:
    res = parse_line(line)
    pos = res[:2]
    vel = res[2:]
    points.append(Point(pos, vel))

def bounds(points, n):
    first_point = points[0].pos_at(n)
    min_x = max_x = first_point[0]
    min_y = max_y = first_point[1]
    for point in points:
        pos = point.pos_at(n)
        if pos[0] < min_x:
            min_x = pos[0]
        if pos[0] > max_x:
            max_x = pos[0]
        if pos[1] < min_y:
            min_y = pos[1]
        if pos[1] > max_y:
            max_y = pos[1]
    return (min_x, max_x, min_y, max_y)

def print_points(points, n, min_x, max_x, min_y, max_y):
    cols = max_x - min_x + 1
    rows = max_y - min_y + 1
    array = [[0]*cols for __ in range(rows)]
    for point in points:
        p = point.pos_at(n)
        col = p[0] - min_x
        row = p[1] - min_y

        array[row][col] = 1
    print("After seconds:", n)
    for row in array:
        line = ['#' if x else ' ' for x in row]
        print(''.join(line))
    print()


for n in range(10940, 10950):
    min_x, max_x, min_y, max_y = bounds(points, n)
    width = max_x - min_x
    print(width)
    if width < 100:
        print_points(points, n, min_x, max_x, min_y, max_y)


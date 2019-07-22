from itertools import product

#filename = 'test.txt'
filename = 'input.txt'
filename = 'repiphany.txt'
import sys
sys.setrecursionlimit(5000)
with open(filename) as f:
    data = f.read().strip().splitlines()

import time
start_time = time.time()

clay_coords = set()
for line in data:
    terms = line.split(', ')
    item = {}
    for term in terms:
        var, val = term.split('=')
        if '.' in val:
            lower, upper = map(int, val.split('..'))
            item[var] = range(lower, upper + 1)
        else:
            item[var] = [int(val)]
    clay_coords.update(product(item['y'], item['x']))

sort_by_x = sorted(clay_coords, key=lambda x:x[1])
sort_by_y = sorted(clay_coords, key=lambda x:x[0])

min_x, max_x = sort_by_x[0][1], sort_by_x[-1][1]
min_y, max_y = sort_by_y[0][0], sort_by_y[-1][0]

import numpy

the_map = numpy.zeros((max_y+1, max(max_x+2, 502)))
for coord in clay_coords:
    y, x = coord
    the_map[y][x] += 1
orig_map = the_map.copy()

sub_map = the_map[0:max_y+1, min_x-1:max_x+2]
import png

im = png.from_array(1-the_map, mode='L;1')
im.save("map.png")

settled_water = numpy.zeros(the_map.shape)
flow_visited = numpy.zeros(the_map.shape)

def flow_water(row, col, direction=None):
    if row > max_y:
        return
    if flow_visited[row][col]:
        return
    if the_map[row][col]:
        return 'wall'
    flow_visited[row][col] = 1
    if row == max_y:
        return
    if the_map[row+1][col]:
        # expand left/right
        to_right = flow_sideways(row, col, 'right')
        to_left = flow_sideways(row, col, 'left')
        if to_right == 'wall' and to_left == 'wall':
            fill_sideways(row, col, 'left')
            fill_sideways(row, col, 'right')
    else:
        flow_water(row+1, col)

def flow_sideways(row, col, direction):
    if direction == 'left':
        delta = -1
    else:
        delta = 1
    if the_map[row][col]:
        return 'wall'
    flow_visited[row][col] = 1
    if the_map[row+1][col] == 0:
        flow_water(row+1, col)
        return 'drop'
    else:
        return flow_sideways(row, col+delta, direction)

def fill_sideways(row, col, direction):
    if direction == 'left':
        delta = -1
    else:
        delta = 1
    if the_map[row][col]:
        return
    settled_water[row][col] = 1
    fill_sideways(row, col+delta, direction)

go_again = True
all_settled_water = numpy.zeros(the_map.shape)
all_flows_visited = numpy.zeros(the_map.shape)
step = 0
while go_again:
    step += 1
    settled_water[:] = 0
    flow_visited[:] = 0
    flow_water(0, 500)
    the_map += settled_water
    all_settled_water += settled_water
    go_again = numpy.any(settled_water)
    all_flows_visited += flow_visited




res =(all_flows_visited + all_settled_water)
res = numpy.where(res>0, 1, 0)

print(numpy.sum(all_flows_visited[min_y:max_y+1,:]>0))


im = png.from_array(1-all_settled_water, mode='L;1')
im.save("settled.png")

im = png.from_array(1-all_flows_visited>0, mode='L;1')
im.save("flows.png")

im = png.from_array(1 - res, mode="L;1")
im.save("combined.png")

from PIL import Image
shape = the_map.shape
img_array = 255*numpy.ones([shape[0], shape[1], 3], dtype=numpy.uint8)
img_array[orig_map==1,:] = [0, 0, 0]
img_array[all_flows_visited>0,:] = [0, 153, 255]
im = Image.fromarray(img_array)
im.save("main.png")

print(numpy.sum(all_settled_water>0))

print("Elapsed: {:.2f}s".format(time.time() - start_time))

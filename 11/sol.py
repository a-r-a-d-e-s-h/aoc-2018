import time
start_time = time.time()

data = 2568

def do_calc(x, y, n):
    val = (x+10)*((x+10)*y + n)
    t = val%1000
    t //= 100
    return t-5

print(do_calc(3,5,8))
print(do_calc(122,79,57))
print(do_calc(217,196,39))
print(do_calc(101,153,71))

grid_size = 300

import numpy

grid = numpy.zeros((grid_size, grid_size))
coords = numpy.arange(grid_size)+1

x_coords = numpy.zeros((grid_size, grid_size))
x_coords[:] = coords

y_coords = numpy.zeros((grid_size, grid_size))
y_coords[:] = coords[:,None]


n = 2568

t = ((x_coords+10)*y_coords + n)%1000
t = (t*(x_coords+10))%1000
t = t//100 - 5

v = t[:grid_size - 2] + t[1:grid_size - 1] + t[2:grid_size]
v = v[:,:grid_size-2] + v[:,1:grid_size-1] + v[:,2:grid_size]

res = numpy.unravel_index(numpy.argmax(v.T), v.shape)

th = t
tv = numpy.concatenate((numpy.zeros((1, grid_size)),t[:-1]))
horiz_compress = th
vert_compress = numpy.zeros((grid_size, grid_size))
square_maxs = numpy.zeros((grid_size+1, grid_size+1))

max_power = 0
max_coord = None
max_square_size = None
for i in range(300):
    square_maxs = square_maxs[:-1,:-1] + horiz_compress + vert_compress
    th = th[1:,1:]
    horiz_compress = horiz_compress[1:,:-1]+th
    tv = tv[1:,1:]
    vert_compress = vert_compress[:-1,1:] + tv
    res = numpy.unravel_index(numpy.argmax(square_maxs.T), square_maxs.shape)
    res_shifted = tuple(x+1 for x in res)
    power = square_maxs.T[res]
    if power >= max_power:
        max_power = power
        max_square_size = i+1
        max_coord = res_shifted

print("{},{},{}".format(max_coord[0], max_coord[1],max_square_size))
print("max power attained:", max_power)
print("Time elapsed: {:.2f}s".format(time.time() - start_time))

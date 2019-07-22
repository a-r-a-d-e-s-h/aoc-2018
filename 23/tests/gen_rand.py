import random
from argparse import ArgumentParser

def gen_1d_rand(n, output):
    bounds = [-10**9, 10**9]
    max_radius = 10**7

    intervals = []
    for i in range(n):
        found = False
        while not found:
            rad = random.randint(1, max_radius)
            center = random.randint(*bounds)
            if (center - rad >= bounds[0]) and (center + rad <= bounds[1]):
                intervals.append((center, rad))
                found = True
    lines = []
    for i in intervals:
        lines.append("{}, {}".format(*i))
    with open(output, 'w') as f:
        f.write('\n'.join(lines))

def gen_hypercuboids(dim, n, output):
    bounds = [-10**9, 10**9]
    max_side_length = 10**8

    rects = []
    for i in range(n):
        rect = []
        for dimension in range(dim):
            found = False
            while not found:
                side_len = random.randint(1, max_side_length)
                coord = random.randint(*bounds)
                if bounds[0] <= coord + side_len <= bounds[1]:
                    rect.extend([coord, coord + side_len])
                    found = True
        rects.append(rect)
    lines = []
    for rect in rects:
        lines.append(','.join(map(str, rect)))
    with open(output, 'w') as f:
        f.write('\n'.join(lines))



if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('n', type=int)
    parser.add_argument('output', type=str)
    args = parser.parse_args()
    gen_hypercuboids(3, args.n, args.output)


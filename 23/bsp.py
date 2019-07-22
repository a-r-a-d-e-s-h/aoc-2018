import numpy

from collections import namedtuple
from operator import attrgetter
from puztools import ints_from_file, taxicab

def part_1(bots):
    max_bot = max(bots, key=attrgetter('r'))
    return sum(taxicab(bot.c, max_bot.c) <= max_bot.r for bot in bots)

class Octant:
    convert_mat = numpy.array([
        [-1, 1, 1],
        [1, -1, 1],
        [1, 1, -1],
        [-1, -1, -1]
    ])
    def __init__(self, array):
        self.array = numpy.array(array)

    @classmethod
    def from_ball(cls, center, radius):
        array = (cls.convert_mat @ center)[numpy.newaxis].T + (-radius, radius)
        return cls(array)

class Node(namedtuple('Node', 'location left right')):
    pass

def octant_tree(octants, depth=0):
    if not octants:
        return None
    axis = depth % 4
    vertices = numpy.concatenate([octant.array[axis] for octant in octants])
    vertices = numpy.unique(vertices)
    median = vertices[len(vertices)//2]
    print(median)




def part_2(bots):
    octants = [Octant.from_ball(bot.c, bot.r) for bot in bots]
    tree = octant_tree(octants)

def main():
    data = ints_from_file('test.txt')
    Bot = namedtuple('Bot', 'c r')
    bots = [Bot(item[:3], item[3]) for item in data]
    print(part_1(bots))
    part_2(bots)

if __name__ == "__main__":
    main()


from collections import namedtuple
from operator import attrgetter
from puztools import taxicab, ints_from_file

data = ints_from_file('input.txt')
Bot = namedtuple('Bot', 'c r')
bots = [Bot(item[:3], item[3]) for item in data]

max_bot = max(bots, key=attrgetter('r'))
count = sum(taxicab(bot.c, max_bot.c) <= max_bot.r for bot in bots)
print(count)


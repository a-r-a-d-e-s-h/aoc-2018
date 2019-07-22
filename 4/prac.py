with open('input.txt') as f:
    lines = f.read().strip().splitlines()
lines.sort()

from collections import defaultdict
import re
import numpy
guard_log = defaultdict(numpy.zeros(60).copy)

current_guard = None
sleep_start = None

for line in lines:
    time, event = line.split('] ')
    minute = int(time[-2:])
    if '#' in event:
        gid = int(re.findall('\d+', event)[0])
        current_guard = guard_log[gid]
    elif event == "falls asleep":
        sleep_start = minute
    elif event == "wakes up":
        current_guard[sleep_start:minute] += 1

def max_on_vals(d, key=None):
    def new_key(x):
        if key is None:
            return d[x]
        else:
            return key(d[x])
    return max(d, key=new_key)

print("Part 1")
gid = max_on_vals(guard_log, key=numpy.sum)
minute = numpy.argmax(guard_log[gid])
print(gid*minute)

print("Part 2")
gid = max_on_vals(guard_log, key=numpy.max)
minute = numpy.argmax(guard_log[gid])
print(gid*minute)


#filename = "test.txt"
filename = "input.txt"

with open(filename) as f:
    lines = f.read().strip().splitlines()

from datetime import datetime

def pt(x):
    fmt = "%Y-%m-%d %H:%M"
    return datetime.strptime(x, fmt)

events = []
for line in lines:
    parts = line.split(']')
    time = parts[0][1:]
    desc = parts[1].strip()
    events.append((pt(time), desc))

events = sorted(events, key=lambda x: x[0])


guards = {}
import re
import numpy
current_guard = None
for time, desc in events:
    if desc == "falls asleep":
        sleep_start = time
    elif desc == "wakes up":
        sleep_end = time
        if current_guard not in guards:
            guards[current_guard] = numpy.zeros(60)
        c = guards[current_guard]
        c[sleep_start.minute:sleep_end.minute] += 1
    else:
        guard_ids = re.findall('\d+', desc)
        current_guard = int(guard_ids[0])

guard_ids = sorted(guards.keys())
max_sleep = 0
max_guard = None
for gid in guard_ids:
    print(gid, numpy.sum(guards[gid]))
    tot_sleep = numpy.sum(guards[gid])
    if tot_sleep > max_sleep:
        max_sleep = tot_sleep
        max_guard = gid

print("Sleepiest guard is:", max_guard)
print("Sleepiest minute is:", numpy.argmax(guards[max_guard]))

print(max_guard * numpy.argmax(guards[max_guard]))

max_sleep = 0
max_guard = None
max_minute = None
for gid in guard_ids:
    minute = numpy.argmax(guards[gid])
    visits = guards[gid][minute]
    if visits > max_sleep:
        max_sleep = visits
        max_guard = gid
        max_minute = minute

print("Guard {} slept during minute {} a total of {} times".format(max_guard, max_minute, max_sleep))
print(max_guard * max_minute)


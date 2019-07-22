import re
import time

from collections import Counter

start_time = time.time()

def solve(filename):
    with open(filename) as f:
        lines = f.read().strip().splitlines()
    intervals = [tuple(map(int, re.findall('-?\d+', line))) for line in lines]
    intervals = [{'center': x[0], 'radius': x[1]} for x in intervals]
    for inter in intervals:
        inter['lower'] = inter['center'] - inter['radius']
        inter['upper'] = inter['center'] + inter['radius']

    lowers = [inter['lower'] for inter in intervals]
    uppers = [inter['upper'] for inter in intervals]
    after_uppers = [u+1 for u in uppers]

    lower_counts = Counter(lowers)
    upper_counts = Counter(uppers)
    after_upper_counts = Counter(after_uppers)
    all_events = sorted(set(lowers + after_uppers))
    summaries = []
    value = 0
    last_change = None
    for evt in all_events:
        change = lower_counts[evt] - after_upper_counts[evt]
        if last_change is not None:
            summaries.append(((last_change, evt-1), value))
        value += change
        last_change = evt

    max_overlaps = max(summaries, key=lambda x: x[1])[1]
    max_intervals = [s for s in summaries if s[1] == max_overlaps]

    # We will take a point in one of the max_intervals, and verify that it really does lie in max_overlaps

    point = float('inf')
    for inter in max_intervals:
        lower, upper = inter[0]
        if lower <= 0 <= upper:
            point = 0
        else:
            if abs(lower) < abs(point):
                point = lower
            if abs(upper) < abs(point):
                point = upper

    count = 0
    for inter in intervals:
        if inter['lower'] <= point <= inter['upper']:
            count += 1
    print("Largest overlap from algorithm:", max_overlaps)
    print("Verified that {} is contained in {} intervals".format(point, count))



def main():
    solve('squares1.txt')

if __name__ == "__main__":
    main()


filename = 'input.txt'
with open(filename) as f:
    lines = f.read().strip().splitlines()

import re
magic_val = int(re.findall('\d+', lines[8])[0])

def do_step(n):
    x = n | (1 << 16)
    y = magic_val
    while x:
        y += x % 256
        y %= (1 << 24)
        y *= 65899
        y %= (1 << 24)
        x >>= 8
    return y

visits = set()

prev_val = 0
while 1:
    val = do_step(prev_val)
    if not visits:
        # part 1
        print(val)
    if val in visits:
        # part 2
        print(prev_val)
        break
    else:
        visits.add(val)
        prev_val = val

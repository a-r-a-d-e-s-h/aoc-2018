a = 2**16
b = 13431073
c = 2**24 - 1
d = 2**8 - 1
e = 2**8
f = 65899

halting = []

def process(x, y):
    shifter = lambda z : ((z&c)*f)&c
    x //= e
    y = shifter(y + (x&d))
    if x < e:
        # y is a halting constant
        if y not in halting:
            halting.append(y)
        x, y = y|a, shifter(b + (y & d))
    return x, y

if __name__ == '__main__':
    # initial values
    x, y = 0|a, ((b&c)*f)&c
    seen = set([(x, y)])
    while not halting:
        x, y = process(x, y)
        seen.add((x, y))
    print(halting[0])
    while True:
        x, y = process(x, y)
        if (x, y) in seen:
            break
        seen.add((x, y))
print(halting[-1])

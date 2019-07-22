with open('input.txt', 'r') as f:
    data = f.read()
#data = "+7, +7, -2, -7, -4".replace(',', '\n')
visited = set()

vals = data.split('\n')
vals = [int(val) for val in vals if val]
running_tot = 0
done = False
while not done:
    for val in vals:
        if running_tot not in visited:
            visited.add(running_tot)
        else:
            print("Visited {} twice!".format(running_tot))
            done = True
            break
        running_tot += val

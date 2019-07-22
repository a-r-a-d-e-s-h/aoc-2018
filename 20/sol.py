filename = 'repiphany.txt'
with open(filename) as f:
    data = f.read().strip()[1:-1]

rooms = dict()
rooms[0, 0] = 0

def walk(regex, loc=(0,0), offset=0):
    cur_loc = loc
    pos = 0
    while 1:
        try:
            char = regex[offset + pos]
        except IndexError:
            return offset + pos
        deltas = {
            'N': (-1, 0),
            'E': (0, 1),
            'S': (1, 0),
            'W': (0, -1)
        }
        if char in deltas:
            d0, d1 = deltas[char]
            next_loc = (cur_loc[0] + d0, cur_loc[1] + d1)
            if next_loc not in rooms:
                rooms[next_loc] = rooms[cur_loc] + 1
            else:
                rooms[next_loc] = min(rooms[next_loc], rooms[cur_loc] + 1)
            cur_loc = next_loc
            pos += 1
        elif char == '|':
            cur_loc = loc
            pos += 1
        elif char == '(':
            pos += walk(regex, loc=cur_loc, offset=offset+pos+1) + 1
        elif char == ')':
            return pos + 1
            
walk(data)

print(max(rooms.values()))
print(sum(1 for room in rooms if rooms[room] >= 1000))

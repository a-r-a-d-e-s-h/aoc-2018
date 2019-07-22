class Road:
    def __init__(self, symb, coord):
        self.neighbours = []
        self.symb = symb
        self.coord = coord

class Cart:
    def __init__(self, location):
        self.location = location
        self.direction = None
        self._next_choice = 'left'

    def get_next_direction(self):
        cur_loc = self.location.coord
        dir_loc = self.direction.coord
        offset = (dir_loc[0] - cur_loc[0], dir_loc[1] - cur_loc[1])
        if self._next_choice == 'straight':
            new_offset = offset
            self._next_choice = 'right'
        elif self._next_choice == 'left':
            new_offset = (-offset[1], offset[0])
            self._next_choice = 'straight'
        elif self._next_choice == 'right':
            new_offset = (offset[1], -offset[0])
            self._next_choice = 'left'
        next_dir = (dir_loc[0] + new_offset[0], dir_loc[1] + new_offset[1])
        return next_dir

    def __str__(self):
        cur_loc = self.location.coord
        dir_loc = self.direction.coord
        offset = (dir_loc[0] - cur_loc[0], dir_loc[1] - cur_loc[1])
        return {
            (0, 1): '>',
            (0, -1): '<',
            (1, 0): 'v',
            (-1, 0): '^'
        }[offset]

#input_file = "test2.txt"
input_file = "input.txt"
input_file = 'corelax.txt'
input_file = 'j416.txt'

with open(input_file, 'r') as f:
    raw_data = f.read()

lines = raw_data.split('\n')
lines = [l for l in lines if l]
first_line = lines[0]
new_lines = []
for line in lines:
    if len(line) < len(first_line):
        line = line + ' '*(len(first_line) - len(line))
    assert len(line) == len(first_line)
    new_lines.append(line)
lines = new_lines

width = len(first_line)
height = len(lines)
print("Grid size: {} x {}".format(width, height))

grid = [[0]*width for __ in range(height)]

def get_nbours(row, col):
    def nbours():
        col_min = max(col-1, 0)
        col_max = min(col+2, width)
        row_min = max(row-1, 0)
        row_max = min(row+2, height)
        for col_ in range(col_min, col_max):
            if col_ != col:
                yield (row, col_)
        for row_ in range(row_min, row_max):
            if row_ != row:
                yield (row_, col)
    return nbours()

for col in range(width):
    for row in range(height):
        tile = lines[row][col]
        if tile != ' ':
            grid[row][col] = Road(tile, (row, col))
done = False
passes = 0
while not done:
    passes += 1
    all_ok = True
    for row in range(height):
        for col in range(width):
            tile = grid[row][col]
            if not isinstance(tile, Road):
                continue
            symb = tile.symb
            if symb in ('-', '>', '<'):
                tile.neighbours = [grid[row][col-1], grid[row][col+1]]
            elif symb in ('|', 'v', '^'):
                tile.neighbours = [grid[row-1][col], grid[row+1][col]]
            elif symb in ('+',):
                tile.neighbours = [grid[row-1][col], grid[row+1][col], grid[row][col-1], grid[row][col+1]]
            elif symb in ('\\', '/'):
                tile.neighbours = []
                for nrow, ncol in get_nbours(row, col):
                    nbour = grid[nrow][ncol]
                    if not isinstance(nbour, Road):
                        continue
                    if tile in nbour.neighbours:
                        tile.neighbours.append(grid[nrow][ncol])
                if len(tile.neighbours) != 2:
                    all_ok = False
    if all_ok:
        done = True
    print("pass {}".format(passes))

carts = []
cart_locations = [[0]*width for __ in range(height)]

for row in range(height):
    for col in range(width):
        tile = grid[row][col]
        if not isinstance(tile, Road):
            continue
        if tile.symb in ('>', '<', '^', 'v'):
            cart = Cart(tile)
            if tile.symb == '>':
                cart.direction = grid[row][col+1]
                tile.symb = '-'
            elif tile.symb == '<':
                cart.direction = grid[row][col-1]
                tile.symb = '-'
            elif tile.symb == '^':
                cart.direction = grid[row-1][col]
                tile.symb = '|'
            elif tile.symb == 'v':
                cart.direction = grid[row+1][col]
                tile.symb = '|'

            cart_locations[row][col] = 1
            carts.append(cart)

print("{} carts".format(len(carts)))

def do_tick(remove_on_collision=True):
    global carts
    cart_locs = {}
    for cart in carts:
        cart_locs[cart.location.coord] = cart
    sorted_locs = list(sorted(cart_locs.keys()))
    carts_to_remove = []
    for location in sorted_locs:
        cart = cart_locs.pop(location)
        if cart in carts_to_remove:
            continue
        direction = cart.direction
        if direction.symb != '+':
            nbours = direction.neighbours
            for nbb in nbours:
                if nbb != cart.location:
                    break
            else:
                raise RuntimeError("Problem...")
            new_dir = nbb
            assert isinstance(nbb, Road)
        else:
            new_dir_r, new_dir_c = cart.get_next_direction()
            new_dir = grid[new_dir_r][new_dir_c]
            assert isinstance(new_dir, Road)
        if direction.coord in cart_locs:
            if not remove_on_collision:
                return direction.coord
            else:
                carts_to_remove.extend([cart, cart_locs[direction.coord]])
        assert isinstance(new_dir, Road)
        cart.direction = new_dir
        assert isinstance(direction, Road)
        cart.location = direction
        cart_locs[direction.coord] = cart
    carts = [cart for cart in carts if cart not in carts_to_remove]
    if carts_to_remove:
        print("Removed {} carts. {} are remaining.".format(len(carts_to_remove), len(carts)))
    if len(carts) == 1:
        return carts[0].location.coord

def print_map():
    cart_locs = {}
    for cart in carts:
        cart_locs[cart.location.coord] = cart
    for row in range(height):
        line = []
        for col in range(width):
            if (row, col) in cart_locs:
                line.append(str(cart_locs[(row,col)]))
                continue
            tile = grid[row][col]
            if not isinstance(tile, Road):
                line.append(' ')
            else:
                line.append(tile.symb)
        print(''.join(line))

while 1:
    res = do_tick(remove_on_collision=False)
    if res is not None:
        print(res)
        break
ticks = 0
while 1:
    ticks += 1
    res = do_tick()
    if res is not None:
        print("Simulation finished on tick: {}".format(ticks))
        print("{},{}".format(res[1], res[0]))
        break


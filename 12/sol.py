with open('repiphany.txt', 'r') as f:
    data = f.read()
lines = data.split('\n')
transforms = lines[2:]
transforms = [line for line in transforms if line]
initial = lines[0][15:]

initial = [int(x == '#') for x in initial]

rules = []
for trans in transforms:
    pattern, res = trans.split('=>')
    pattern = pattern.strip()
    pattern = [int(x=='#') for x in pattern]
    res = int(res.strip() == '#')
    rules.append((pattern, res))


class Pot:
    min_index = None
    max_index = None
    def __init__(self, index, val):
        self.index = index
        self.val = val
        self.next_val = None
        self.next = None
        self.prev = None

    def ins_next(self, nbour):
        self.next = nbour
        nbour.prev = self

    def ins_prev(self, nbour):
        self.prev = nbour
        nbour.next = self

initial_pots = []
for i, value in enumerate(initial):
    initial_pots.append(Pot(i, value))
    if i > 0:
        initial_pots[-1].ins_prev(initial_pots[-2])


def get_neighbours(pot, left=2, right=2):
    cur_pot = pot
    next_vals = []
    for j in range(right):
        if cur_pot is not None:
            next_pot = cur_pot.next
            if next_pot is not None:
                next_vals.append(next_pot.val)
                cur_pot = next_pot
                continue
        next_vals.append(0)
    prev_vals = []
    cur_pot = pot
    for j in range(left):
        if cur_pot is not None:
            prev_pot = cur_pot.prev
            if prev_pot is not None:
                prev_vals.append(prev_pot.val)
                cur_pot = prev_pot
                continue
        prev_vals.append(0)
    return prev_vals[-1::-1] + [pot.val] + next_vals

def get_next_state(pot, rules):
    nbours = get_neighbours(pot)
    for rule in rules:
        if nbours == rule[0]:
            return rule[1]
    else:
        return 0

def update_states(pot):
    is_next = True
    next_pot = pot
    states_right = []
    nums_right = []
    while is_next:
        cur_pot = next_pot
        cur_pot.val = cur_pot.next_val
        states_right.append(cur_pot.val)
        nums_right.append(cur_pot.val * cur_pot.index)
        next_pot = cur_pot.next
        is_next = (next_pot is not None)
    cur_pot = pot
    prev_pot = pot.prev
    is_prev = (prev_pot is not None)
    states_left = []
    nums_left = []
    while is_prev:
        cur_pot = prev_pot
        cur_pot.val = cur_pot.next_val
        states_left.append(cur_pot.val)
        nums_left.append(cur_pot.val * cur_pot.index)
        prev_pot = cur_pot.prev
        is_prev = (prev_pot is not None)
    return nums_left[-1::-1] + nums_right

def apply_iteration(pot, rules, add_extra=2):
    is_next = True
    next_pot = pot
    while is_next:
        cur_pot = next_pot
        cur_pot.next_val = get_next_state(cur_pot, rules)
        next_pot = cur_pot.next
        if next_pot is None:
            is_next = False

    for count in range(add_extra):
        cur_pot.ins_next(Pot(cur_pot.index+1, 0))
        cur_pot = cur_pot.next
        cur_pot.next_val = get_next_state(cur_pot, rules)

    cur_pot = pot
    prev_pot = pot.prev
    is_prev = (prev_pot is not None)
    while is_prev:
        cur_pot = prev_pot
        cur_pot.next_val = get_next_state(cur_pot, rules)
        prev_pot = cur_pot.prev
        is_prev = (prev_pot is not None)

    for count in range(add_extra):
        cur_pot.ins_prev(Pot(cur_pot.index-1, 0))
        cur_pot = cur_pot.prev
        cur_pot.next_val = get_next_state(cur_pot, rules)


    return update_states(pot)
iterations = 50000000000
state = []
seq = []

vals = []

def is_cycling(vals):
    if len(vals) < 10:
        return None
    num_vals = len(vals)
    last_ten = vals[-10:]
    delta = last_ten[1] - last_ten[0]
    if all(last_ten[i+1] -last_ten[i] == delta for i in range(9)):
        def f(n):
            x = vals[-1] - delta*num_vals
            return delta*n + x
        return f

for i in range(iterations):
    state = apply_iteration(initial_pots[0], rules)
    val = sum(state)
    print(i, val)
    vals.append(val)
    f = is_cycling(vals)
    if f:
        print("...")
        print(f(iterations))
        break

#part 1: 11:55
with open('input.txt', 'r') as f:
    data = f.read()
#data = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"

node_count = 0
running_tot = 0

def parse_data(data):
    global node_count
    node_count += 1
    node_num = node_count
    num_children = data[0]
    num_meta = data[1]
    length = 2
    print('starting', node_num)
    child_vals = []
    for i in range(num_children):
        new_len, child_val = parse_data(data[length:])
        child_vals.append(child_val)
        length += new_len
    metas = data[length:length+num_meta]
    length += num_meta
    print('finished', node_num, metas)
    global running_tot
    running_tot += sum(metas)
    if num_children == 0:
        node_val = sum(metas)
    else:
        node_val = 0
        for i in metas:
            index = i-1
            if 0 <= index < num_children:
                node_val += child_vals[index]
    return length, node_val

data = data.split(' ')
data = [int(x) for x in data]
legth, val = parse_data(data)
print(running_tot)
print(val)

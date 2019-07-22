filename='input.txt'
with open(filename) as f:
    lines = f.read().strip().splitlines()

def addr(a, b, c, registers):
    registers[c] = registers[a] + registers[b]

def addi(a, b, c, registers):
    registers[c] = registers[a] + b

def mulr(a, b, c, registers):
    registers[c] = registers[a]*registers[b]

def muli(a, b, c, registers):
    registers[c] = registers[a]*b

def banr(a, b, c, registers):
    registers[c] = registers[a] & registers[b]

def bani(a, b, c, registers):
    registers[c] = registers[a] & b

def borr(a, b, c, registers):
    registers[c] = registers[a] | registers[b]

def bori(a, b, c, registers):
    registers[c] = registers[a] | b

def setr(a, b, c, registers):
    registers[c] = registers[a]

def seti(a, b, c, registers):
    registers[c] = a

def gtir(a, b, c, registers):
    registers[c] = int(a > registers[b])

def gtri(a, b, c, registers):
    registers[c] = int(registers[a] > b)

def gtrr(a, b, c, registers):
    registers[c] = int(registers[a] > registers[b])

def eqir(a, b, c, registers):
    registers[c] = int(a == registers[b])

def eqri(a, b, c, registers):
    registers[c] = int(registers[a] == b)

def eqrr(a, b, c, registers):
    registers[c] = int(registers[a] == registers[b])

ops = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
op_names = [op.__name__ for op in ops]
import re
def parse_line(line):
    parts = line.split(' ')
    op_code = parts[0]
    params = tuple(int(x) for x in parts[1:])
    return (ops[op_names.index(op_code)], params)

class Instruction:
    halt = None
    def __init__(self, line, line_number):
        parts = line.split(' ')
        op_code = parts[0]
        self.params = tuple(int(x) for x in parts[1:])
        self.op = ops[op_names.index(op_code)]
        self.line_number = line_number
        self.goto = []

    def call(self, registers):
        a, b, c = self.params
        self.op(a, b, c, registers)

    def __repr__(self):
        return "{}: {} {} {} {}".format(self.line_number, self.op.__name__, *self.params)


evt_lines = [l for l in lines if l[0] != '#']
evts = [Instruction(l, index) for index, l in enumerate(evt_lines) if l[0] != '#']

class InstructionPointer:
    def __init__(self, registers):
        self.val = 0
        self.registers = registers
        self.bind = None

    def bind_to_register(self, r):
        self.bind = r

    def get_val(self):
        if self.bind is None:
            return self.val
        else:
            return self.registers[self.bind]

    def set_val(self, v):
        if self.bind is None:
            self.val = v
        else:
            self.registers[self.bind] = v

    def inc_val(self):
        self.set_val(self.get_val() + 1)


ptrs = [int(l[4:]) for l in lines if '#' == l[0]]
ptr = ptrs[0]
print(ptr)

def find_ptr_mods(evts, ptr):
    return [evt for evt in evts if evt.params[2] == ptr]

mods = find_ptr_mods(evts, ptr)
for mod in mods:
    print(mod)

def map_routes(evts, ptr):
    for index, evt in enumerate(evts):
        if evt.params[2] != ptr:
            try:
                next_evt = evts[index+1]
            except IndexError:
                pass
            else:
                if next_evt not in evt.goto:
                    evt.goto.append(next_evt)
        else:
            if evt.op == seti:
                next_evt = evts[evt.params[0] + 1]
                if next_evt not in evt.goto:
                    evt.goto.append(next_evt)
            elif evt.op == addi:
                if evt.params[0] == ptr:
                    next_evt = evts[index + evt.params[1] + 1]
                    if next_evt not in evt.goto:
                        evt.goto.append(next_evt)
                else:
                    raise NotImplementedError
            elif evt.op == setr:
                raise NotImplementedError
            elif evt.op == addr:
                regs = evt.params[0:2]
                if ptr not in regs:
                    raise NotImplementedError
                reg = regs[regs[0] == ptr]
                setters = find_setters(evts, reg, index)
                full_range = set()
                for e in setters:
                    if e.op in [gtir, gtri, gtrr, eqir, eqri, eqrr]:
                        full_range.update(range(2))
                    else:
                        raise RuntimeError
                for val in sorted(full_range):
                    try:
                        next_evt = evts[index + val + 1]
                    except IndexError:
                        next_evt = Instruction.halt
                    finally:
                        if next_evt not in evt.goto:
                            evt.goto.append(next_evt)

def find_setters(evts, reg, index):
    visited = [0]*len(evts)
    to_do = [index]
    setters = []
    while to_do:
        i = to_do.pop()
        if visited[i]:
            continue
        visited[i] = 1
        evt = evts[i]
        op = evt.op
        params = evt.params
        if params[2] == reg:
            setters.append(evt)
            continue
        to_do.extend(e.line_number for e in evts if evt in e.goto if e)
    return setters

map_routes(evts, ptr)

for evt in evts:
    ln = evt.line_number
    gotos = [str(e.line_number) if e else "HALT" for e in evt.goto]
    print("{}:".format(ln), ", ".join(gotos))


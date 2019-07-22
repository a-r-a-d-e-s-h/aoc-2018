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

evts = [parse_line(l) for l in lines if l[0] != '#']

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

def run(code, registers):
    pointer_instructions = [l for l in code if l[0] == '#']
    evts = [parse_line(l) for l in code if l[0] != '#']
    pointer = InstructionPointer(registers)
    if pointer_instructions:
        val = int(re.findall('\d+', pointer_instructions[0])[0])
        pointer.bind_to_register(val)
    steps = 0
    visits = set()
    while 1:
        steps += 1
        index = pointer.get_val()
        if index == 28:
            if registers[3] in visits:
                print("Part 2")
                print(registers[3])
            else:
                visits.add(registers[3])
                print("Adding", registers[3])
        if index < 0 or index >= len(evts):
            break
        evt = evts[index]
        a, b, c = evt[1]
        evt[0](a, b, c, registers)
        pointer.inc_val()
    print("{} steps".format(steps))
    return registers

def do_debug(index, steps, registers):
    if index == 14 and False:
        print("{}:".format(steps), registers)
        if 256 > registers[2]:
            print("r[2] < 256, jumping to 28")
        else:
            print("r[2] >= 256, jumping to 17")
    if index == 28:
        print("{}:".format(steps), registers)
        if registers[0] == registers[3]:
            print("r[0] == r[3], ending!")
        else:
            print("r[0] != r[3], jumping to 6")

run(lines, [0, 0, 0, 0, 0, 0])


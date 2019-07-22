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


registers = [0] * 6

pointer = InstructionPointer(registers)
pointer.bind_to_register(4)

r = registers

vals = set()

r[3] = 123
while 1:
    r[3] &= 456
    r[3] = int(r[3] == 72)
    if r[3]:
        continue
    else:
        break
r[3] = 0
break_outer = False
while not break_outer:
    print(r)
    r[2] = r[3] | 65536
    r[3] = 7637914
    while not break_outer:
        r[1] = r[2] & 255
        r[3] += r[1]
        r[3] &= 16777215
        r[3] *= 65899
        r[3] &= 16777215
        r[1] = int(256 > r[2])
        if r[1]:
            r[1] = int(r[3] == r[0])
            if r[1]:
                break_outer = True
                break # end
            else:
                print(r[3])
                break # goto 6
        else:
            r[1] = 0
            while 1:
                r[5] = r[1] + 1
                r[5] *= 256
                r[5] = int(r[5] > r[2])
                if r[5]:
                    r[2] = r[1]
                    break #goto 8
                else:
                    r[1] += 1
                    continue  #goto 18


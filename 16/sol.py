input_file = "input.txt"
registers = [0]*4

def reset_registers():
    registers[:] = [0]*4

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

with open(input_file) as f:
    data = f.read().strip()

# data is split into examples and code by three empty lines

ex_text, code = data.split('\n\n\n')

ex_lines = ex_text.splitlines()
ex_lines = [l.strip() for l in ex_lines if l.strip()]

assert len(ex_lines)%3 == 0
examples = []
import re
for i in range(len(ex_lines)//3):
    offset = i*3
    before = tuple(map(int, re.findall('-?\d+', ex_lines[offset])))
    offset += 1
    instruction = tuple(map(int, re.findall('-?\d+', ex_lines[offset])))
    offset += 1
    after = tuple(map(int, re.findall('-?\d+', ex_lines[offset])))
    examples.append((before, instruction, after))

print("Now to identify ops")
op_map = {}
to_do = True
while len(op_map) < len(ops):
    consistent = [list(op for op in ops if op not in op_map.values()) for op in ops]
    for before, instruction, after in examples:
        for op in ops:
            op_code, a, b, c = instruction
            if op not in consistent[op_code]:
                continue
            before_copy = list(before)
            op(a, b, c, before_copy)
            if tuple(before_copy) != after:
                consistent[op_code].remove(op)
    for i in range(len(ops)):
        if len(consistent[i]) == 1:
            op_map[i] = consistent[i][0]
    print("identified:", len(op_map))

print("Check consistent with examples...")

all_ok = True
for before, instruction, after in examples:
    op_code, a, b, c = instruction
    op = op_map[op_code]
    before_copy = list(before)
    op(a, b, c, before_copy)
    if tuple(before_copy) != after:
        all_ok = False
        break
if all_ok:
    print("All consistent :)")
else:
    print("Inconsistent :(")

print("Part 1")
answer = 0
for before, instruction, after in examples:
    op_code, a, b, c = instruction
    consistent_count = 0
    for op in ops:
        before_copy = list(before)
        op(a, b, c, before_copy)
        if tuple(before_copy) == after:
            consistent_count += 1
    if consistent_count >= 3:
        answer += 1
print(answer)

print("Part 2")

lines = code.splitlines()
instructions = [tuple(map(int, re.findall('-?\d+', l))) for l in lines if l.strip()]

registers = [0]*4

for op_code, a, b, c in instructions:
    op = op_map[op_code]
    op(a, b, c, registers)

print(registers[0])
print(registers)

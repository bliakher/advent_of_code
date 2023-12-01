stacks = [
    ['B', 'Z', 'T'],
    ['V', 'H', 'T', 'D', 'N'],
    ['B', 'F', 'M', 'D'],
    ['T', 'J', 'G', 'W', 'V', 'Q', 'L'],
    ['W', 'D', 'G', 'P', 'V', 'F', 'Q', 'M'],
    ['V', 'Z', 'Q', 'G', 'H', 'F', 'S'],
    ['Z', 'S', 'N', 'R', 'L', 'T', 'C', 'W'],
    ['Z', 'H', 'W', 'D', 'J', 'N', 'R', 'M'],
    ['M', 'Q', 'L', 'F', 'D', 'S']
]

def read_input(file_name):
    res = []
    with open(file_name) as f:
        for line in f.readlines():
            instr = line.strip()
            res.append(instr)
    return res

def rearrange(stacks, instructions):
    for instruction in instructions:
        instr_parts = instruction.split(' ')
        quantity = int(instr_parts[1])
        fr = int(instr_parts[3]) - 1
        to = int(instr_parts[5]) - 1
        stack_from = stacks[fr]
        stack_to = stacks[to]
        for i in range(quantity):
            item = stack_from.pop()
            stack_to.append(item)

def rearrange2(stacks, instructions):
    for instruction in instructions:
        instr_parts = instruction.split(' ')
        quantity = int(instr_parts[1])
        fr = int(instr_parts[3]) - 1
        to = int(instr_parts[5]) - 1
        stack_from = stacks[fr]
        stack_to = stacks[to]
        moving = []
        for i in range(quantity):
            item = stack_from.pop()
            moving.append(item)
        for i in range(len(moving)):
            item = moving.pop()
            stack_to.append(item)

def get_top(stacks):
    res = ''
    for stack in stacks:
        top = stack.pop()
        res += top
    return res

instructions = read_input('instructions.txt')
rearrange2(stacks, instructions)
print(get_top(stacks))

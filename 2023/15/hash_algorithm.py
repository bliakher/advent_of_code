
class Lens:
    def __init__(self, label: str, focal: int) -> None:
        self.label = label
        self.focal = focal

def read_input(file_name) -> list[str]:
    result = []
    with open(file_name) as f:
        line = f.readline().strip()
        result = line.split(',')
    return result

def hash(str: str) -> int:
    result = 0
    for c in str:
        result += ord(c)
        result *= 17
        result = result % 256
    return result

def get_hash_sum(instructions: list[str]) -> int:
    sum = 0
    for instr in instructions:
        h = hash(instr)
        sum += h
    return sum

def parse_instruction(instruction: str):
    if '=' in instruction:
        parts = instruction.split('=')
        label = parts[0]
        focus = int(parts[1])
        return True, Lens(label, focus)
    label = instruction.split('-')[0]
    return False, Lens(label, -1)

def find_lens(label:str, lenses: list[Lens]) -> int:
    idx = -1
    for i in range(len(lenses)):
        lens = lenses[i]
        if lens.label == label:
            idx = i
            break
    return idx

def perform_initialization_sequence(instructions: list[str]) -> int:
    boxes = {}
    for instr in instructions:
        add, parsed = parse_instruction(instr)
        box = hash(parsed.label)
        if not box in boxes:
            boxes[box] = []
        lenses: list[Lens] = boxes[box]
        if add:
            found_idx = find_lens(parsed.label, lenses)
            if found_idx != -1:
                lenses[found_idx] = parsed
            else:
                lenses.append(parsed)
        else:
            found_idx = find_lens(parsed.label, lenses)
            if found_idx != -1:
                lenses.pop(found_idx)
        boxes[box] = lenses
        print(boxes)
    
    sum = 0
    for (box, lenses) in boxes.items():
        for lens_idx in range(len(lenses)):
            lens = lenses[lens_idx]
            focusing_power = (box + 1) * (lens_idx + 1) * lens.focal
            sum += focusing_power
    return sum




instructions = read_input('input.txt')
# instructions = read_input('/Users/evgeniagolubeva/advent_of_code/2023/15/input_small.txt')

res = get_hash_sum(instructions)
print(res)

res2 = perform_initialization_sequence(instructions)
print(res2)
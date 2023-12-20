
def read_input(file_name) -> list[list[str]]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            row = []
            for c in line.strip():
                row.append(c)
            result.append(row)
    return result

def get_next_direction(direction: list[int], element: str) -> list[list[int]]:
    x =  direction[0]
    y = direction[1]
    if element == '/':
        return [[y * -1, x * -1]]
    if element == '\\':
        return [[y, x]]
    if element == '-':
        if y == 0: # -> -
            return [direction]
        return [[1, 0], [-1, 0]]
    if element == '|':
        if x == 0:
            return [direction]
        return [[0, 1], [0, -1]]

def move(position: list[int], direction: list[int]) -> list[int]:
    return [position[0] + direction[0], position[1] + direction[1]]

def is_inside(position: list[int], contraption: list[list[str]]) -> bool:
    return position[0] >= 0 and position[0] < len(contraption[0]) and position[1] >= 0 and position[1] < len(contraption)



def pass_light(start_pos:list[int], start_dir: list[int], contraption: list[list[str]]) -> int:
    visited = set()
    visited_with_dir = set()
    stack = []
    start_beam = [start_pos, start_dir]
    stack.append(start_beam)
    while len(stack) > 0:
        cur_beam = stack.pop(-1)
        cur_pos = cur_beam[0]
        cur_dir = cur_beam[1]

        pos_str = f"{cur_pos[0]} {cur_pos[1]}"
        pos_dir_str = f"{cur_pos[0]} {cur_pos[1]}-{cur_dir[0]} {cur_dir[1]}"
        if not pos_str in visited:
            visited.add(pos_str)
        if pos_dir_str in visited_with_dir:
            continue
        else:
            visited_with_dir.add(pos_dir_str)

        next_pos = move(cur_pos, cur_dir)
        if not is_inside(next_pos, contraption):
            continue
        element = contraption[next_pos[1]][next_pos[0]]
        if element == '.':
            stack.append([next_pos, cur_dir])
        else:
            next_dirs = get_next_direction(cur_dir, element)
            for next_dir in next_dirs:
                stack.append([next_pos, next_dir])
    
    return len(visited) - 1 # starting outside of contraption
        

def try_all_starts(contraption: list[list[str]]) -> int:
    max_energized = 0
    for i in range(len(contraption)):
        from_left = pass_light([-1, i], [1, 0], contraption)
        from_right = pass_light([len(contraption), i], [-1, 0], contraption)
        if max(from_left, from_right) > max_energized:
            max_energized = max(from_left, from_right)

    for i in range(len(contraption[0])):
        from_up = pass_light([i, -1], [0, 1], contraption)
        from_down = pass_light([1, len(contraption[0])], [0, -1], contraption)
        if max(from_up, from_down) > max_energized:
            max_energized = max(from_up, from_down)

    return max_energized


contraption = read_input('input.txt')
contraption = read_input('input_small.txt')

res = pass_light([-1, 0], [1, 0], contraption)
print(res)

res2 = try_all_starts(contraption)
print(res2)
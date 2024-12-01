
def read_input(file_name) -> list[list[str]]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            row = []
            for c in line.strip():
                row.append(c)
            result.append(row)
    return result

def move_rock_north(y: int, x: int, platform: list[list[str]]):
    found_free = False
    cur_target_y = 0
    for i in range(y - 1, -1, -1):
        if platform[i][x] == '.':
            found_free = True
            cur_target_y = i
        else:
            break # cannot go further, there is a rock -> stop
    if found_free:
        platform[cur_target_y][x] = platform[y][x]
        platform[y][x] = '.'

def move_rock_south(y: int, x: int, platform: list[list[str]]):
    found_free = False
    cur_target_y = 0
    for i in range(y + 1, len(platform), 1):
        if platform[i][x] == '.':
            found_free = True
            cur_target_y = i
        else:
            break # cannot go further, there is a rock -> stop
    if found_free:
        platform[cur_target_y][x] = platform[y][x]
        platform[y][x] = '.'

def move_rock_west(y: int, x: int, platform: list[list[str]]):
    found_free = False
    cur_target_x = 0
    for j in range(x - 1, -1, -1):
        if platform[y][j] == '.':
            found_free = True
            cur_target_x = j
        else:
            break # cannot go further, there is a rock -> stop
    if found_free:
        platform[y][cur_target_x] = platform[y][x]
        platform[y][x] = '.'

def move_rock_east(y: int, x: int, platform: list[list[str]]):
    found_free = False
    cur_target_x = 0
    for j in range(x + 1, len(platform[0]), 1):
        if platform[y][j] == '.':
            found_free = True
            cur_target_x = j
        else:
            break # cannot go further, there is a rock -> stop
    if found_free:
        platform[y][cur_target_x] = platform[y][x]
        platform[y][x] = '.'

def tilt_to_north(platform: list[list[str]]) -> None:
    for i in range(1, len(platform)): # skip first row - cannot move further
        for j in range(len(platform[0])):
            if platform[i][j] == 'O':
                move_rock_north(i, j, platform)

def tilt_to_north2(platform: list[list[str]]) -> None:
    for j in range(len(platform[0])):
        last_occupied_y = -1
        for i in range(len(platform)):
            if platform[i][j] == 'O':
                free = last_occupied_y + 1
                if free != i:
                    platform[free][j] = platform[i][j]
                    platform[i][j] = '.'
                last_occupied_y = free
            if platform[i][j] == '#':
                last_occupied_y = i


def tilt_to_south(platform: list[list[str]]) -> None:
    for i in range(len(platform) - 2, -1, -1): # skip first row - cannot move further
        for j in range(len(platform[0])):
            if platform[i][j] == 'O':
                move_rock_south(i, j, platform)

def tilt_to_south2(platform: list[list[str]]) -> None:
    for j in range(len(platform[0])): # skip first row - cannot move further
        last_occupied_y = len(platform)
        for i in range(len(platform) - 1, -1, -1):
            if platform[i][j] == 'O':
                free = last_occupied_y - 1
                if free != i:
                    platform[free][j] = platform[i][j]
                    platform[i][j] = '.'
                last_occupied_y = free
            if platform[i][j] == '#':
                last_occupied_y = i

def tilt_to_west(platform: list[list[str]]) -> None:
    for j in range(1, len(platform[0])): # skip first row - cannot move further
        for i in range(len(platform)):
            if platform[i][j] == 'O':
                move_rock_west(i, j, platform)

def tilt_to_west2(platform: list[list[str]]) -> None:
    for i in range(len(platform)):
        last_occupied_x = -1
        for j in range(len(platform[0])):
            if platform[i][j] == 'O':
                free = last_occupied_x + 1
                if free != j:
                    platform[i][free] = platform[i][j]
                    platform[i][j] = '.'
                last_occupied_x = free
            if platform[i][j] == '#':
                last_occupied_x = j

def tilt_to_east(platform: list[list[str]]) -> None:
    for j in range(len(platform[0]) - 2, -1, -1): # skip first row - cannot move further
        for i in range(len(platform)):
            if platform[i][j] == 'O':
                move_rock_east(i, j, platform)

def tilt_to_east2(platform: list[list[str]]) -> None:
    for i in range(len(platform)):
        last_occupied_x = len(platform[0])
        for j in range(len(platform[0]) - 1, -1, -1):
            if platform[i][j] == 'O':
                free = last_occupied_x - 1
                if free != j:
                    platform[i][free] = platform[i][j]
                    platform[i][j] = '.'
                last_occupied_x = free
            if platform[i][j] == '#':
                last_occupied_x = j

def do_spin_cycle(platform: list[list[str]]) -> None:
    tilt_to_north(platform)
    tilt_to_west(platform)
    tilt_to_south(platform)
    tilt_to_east(platform)

def do_spin_cycle2(platform: list[list[str]]) -> None:
    tilt_to_north2(platform)
    tilt_to_west2(platform)
    tilt_to_south2(platform)
    tilt_to_east2(platform)

def check_all_prev(prev, new) -> bool:
    same = None
    found = False
    for i in range(len(prev)):
        item = prev[i]
        if check_same(item, new):
            same = item
            found = True
            break
    if found:
        print('same as', i)
    return found


def run_spin_cycle(count: int, platform: list[list[str]]) -> None:
    prev = []
    for i in range(count):
        do_spin_cycle2(platform)
        if i == 91:
            break
        if len(prev) > 0:
            if check_all_prev(prev, platform):
                print('found', i)
                # break
        prev.append(make_platform_copy(platform))
        print(i)

def check_same(plat1: list[list[str]], plat2: list[list[str]]) -> bool:
    same = True
    for i in range(len(platform)):
        for j in range(len(platform[0])):
            if plat1[i][j] != plat2[i][j]:
                same = False
    return same


def make_platform_copy(platform: list[list[str]]) -> list[list[str]]:
    res = []
    for row in platform:
        res.append(row.copy())
    return res

def calculate_load_north(platform: list[list[str]]) -> int:
    load = 0
    for i in range(len(platform)):
        cur_load_coef = len(platform) - i
        for j in range(len(platform[0])):
            if platform[i][j] == 'O':
                load += cur_load_coef
    return load


def print_platform(platform: list[list[str]]) -> None:
    for row in platform:
        for c in row:
            print(c, end='')
        print()

platform = read_input('input.txt')
# platform = read_input('/Users/evgeniagolubeva/advent_of_code/2023/14/input_small.txt')

# print_platform(platform)
# copy = make_platform_copy(platform)
# tilt_to_north(platform)
# print_platform(platform)
# print('-------------------')

# tilt_to_north2(copy)
# print_platform(copy)
# assert check_same(platform, copy)

# print('----------------------------------')

# tilt_to_south(platform)
# print_platform(platform)
# print('-------------------')

# tilt_to_south2(copy)
# print_platform(copy)
# assert check_same(platform, copy)

# print('----------------------------------')

# tilt_to_west(platform)
# print_platform(platform)
# print('-------------------')

# tilt_to_west2(copy)
# print_platform(copy)
# assert check_same(platform, copy)

# print('----------------------------------')


# tilt_to_east(platform)
# print_platform(platform)
# print('-------------------')

# tilt_to_east2(copy)
# print_platform(copy)
# assert check_same(platform, copy)

# do_spin_cycle(platform)
# do_spin_cycle2(copy)
# assert check_same(platform, copy)


run_spin_cycle(1_000_000_000, platform)


# print_platform(platform)

res = calculate_load_north(platform)
print(res)
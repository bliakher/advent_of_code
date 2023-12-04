from typing import *

def read_input(file_name) -> list[list[str]]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            str = line.strip()
            row = []
            for char in str:
                row.append(char)
            result.append(row)
    return result

def is_in_schematic(row: int, col: int, schematic: list[list[str]]):
    return row >= 0 and col >= 0 and row < len(schematic) and col < len(schematic[0])

def is_next_to_symbol(row: int, col: int, schematic: list[list[str]]) -> bool:
    neighbors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    for neighbor in neighbors:
        n_row = row + neighbor[0]
        n_col = col + neighbor[1]
        if not is_in_schematic(n_row, n_col, schematic):
            continue
        n_char = schematic[n_row][n_col]
        if not n_char.isdigit() and n_char != '.':
            return True
    return False

def find_part_numbers(schematic: list[list[str]]) -> int:
    sum = 0
    for row_idx in range(len(schematic)):
        row = schematic[row_idx]
        reading_part = False
        next_to_symbol = False
        cur_num = 0
        for col_idx in range(len(row)):
            char = row[col_idx]
            if char.isdigit():
                reading_part = True
                i = int(char)
                cur_num = cur_num * 10 + i
                next_to_symbol = next_to_symbol or is_next_to_symbol(row_idx, col_idx, schematic)

            elif reading_part:
                print(cur_num, next_to_symbol)
                if next_to_symbol:
                    sum += cur_num
                reading_part = False
                next_to_symbol = False
                cur_num = 0
        if reading_part:
            print(cur_num, next_to_symbol)
            if next_to_symbol:
                sum += cur_num
    return sum


def is_next_to_symbol2(row: int, col: int, schematic: list[list[str]]) -> (bool, Set[int]):
    neighbors = [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
    result = False
    gear_positions: Set[int] = set()
    for neighbor in neighbors:
        n_row = row + neighbor[0]
        n_col = col + neighbor[1]
        if not is_in_schematic(n_row, n_col, schematic):
            continue
        n_char = schematic[n_row][n_col]
        if not n_char.isdigit() and n_char != '.':
            result = True
            if n_char == '*':
                gear_positions.add(get_gear_id(n_row, n_col))
    return (result, gear_positions)

def get_gear_id(row, col) -> int:
    return (row + 1) * 1000 + col + 1

def update_gears(part_num: int, gears: Set[int], candidates: Dict[int, int], results: Dict[int, int]):
    # print(part_num, gears)
    # print('before', candidates, results)
    for id in gears:
        if id in candidates:
            value = candidates[id] * part_num
            candidates.pop(id, None)
            results[id] = value
        elif id in results:
            results[id] = -1
        else:
            candidates[id] = part_num
    # print('after', candidates, results)
    return (candidates, results)

def get_gear_sum(results: Dict[int, int]) -> int:
    sum = 0
    for id in results:
        value = results[id]
        if value != -1:
            sum += value
    return sum

def find_gear_ratios(schematic: list[list[str]]) -> int:
    candidates = {}
    results = {}
    for row_idx in range(len(schematic)):
        row = schematic[row_idx]
        reading_part = False
        next_to_symbol = False
        cur_num = 0
        gear_positions: Set[int] = set()
        for col_idx in range(len(row)):
            char = row[col_idx]
            if char.isdigit():
                reading_part = True
                i = int(char)
                cur_num = cur_num * 10 + i
                next, gears = is_next_to_symbol2(row_idx, col_idx, schematic)
                next_to_symbol = next_to_symbol or next
                gear_positions.update(gears)

            elif reading_part:
                # print(cur_num, next_to_symbol)
                if next_to_symbol:
                    candidates, results = update_gears(cur_num, gear_positions, candidates, results)
                reading_part = False
                next_to_symbol = False
                cur_num = 0
                gear_positions = set()
        if reading_part:
            # print(cur_num, next_to_symbol)
            if next_to_symbol:
                candidates, results = update_gears(cur_num, gear_positions, candidates, results)
    
    # print(candidates, results)
    return get_gear_sum(results)

# input = read_input('input_small.txt')
input = read_input('input.txt')

# res = find_part_numbers(input)
# print(res)

res2 = find_gear_ratios(input)
print(res2)


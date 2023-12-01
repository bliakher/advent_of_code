def read_input_to_list(file_name):
    res = []
    with open(file_name) as f:
        for line in f.readlines():
            num = line.strip()
            res.append(num)
    return res

def find_duplicate(first_half, second_half):
    unique = set()
    for item in first_half:
        unique.add(item)
    duplicate = ''
    for item in second_half:
        if item in unique:
            duplicate = item
            break
    return duplicate

def get_priority(item):
    return ord(item) - 96 if item.islower() else ord(item) - 65 + 27


def fix_rucksacks(file_name):
    sum = 0
    input = read_input_to_list(file_name)
    for rucksack in input:
        first_half = rucksack[ :len(rucksack) // 2]
        second_half = rucksack[len(rucksack) // 2: ]
        duplicate = find_duplicate(first_half, second_half)
        priority = get_priority(duplicate)
        # print(priority)
        sum += priority
    return sum


res = fix_rucksacks('input.txt')
print(res)

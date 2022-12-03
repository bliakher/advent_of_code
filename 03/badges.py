
def read_input_to_list(file_name):
    res = []
    group = []
    with open(file_name) as f:
        for line in f.readlines():
            num = line.strip()
            group.append(num)
            if len(group) == 3:
                res.append(group)
                group = []
    return res

def find_duplicate(first, second_half):
    unique = set()
    duplicates = []
    for item in first:
        unique.add(item)
    for item in second_half:
        if item in unique:
            duplicates.append(item)
    return duplicates

def find_duplicate_3(first, second, last):
    part = find_duplicate(first, second)
    result = find_duplicate(part, last)
    return result[0]

def get_priority(item):
    return ord(item) - 96 if item.islower() else ord(item) - 65 + 27

def find_badges(file_name):
    sum = 0
    input = read_input_to_list(file_name)
    for group in input:
        badge = find_duplicate_3(group[0], group[1], group[2])
        priority = get_priority(badge)
        sum += priority
    return sum

res = find_badges('input.txt')
print(res)
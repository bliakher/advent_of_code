
def read_input(file_name):
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            parts = line.strip().split()
            nums = list(map(lambda x: int(x), parts[1].split(',')))
            result.append([parts[0], nums])
    return result

def read_input2(file_name):
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            parts = line.strip().split()
            nums = list(map(lambda x: int(x), parts[1].split(',')))
            result.append([((parts[0] + "?") * 5)[:-1], nums * 5])
    return result

cache = {}
def count_options(record: str, counts: list[int]):
    global cache

    if len(record) == 0:
        return 1 if len(counts) == 0 else 0
    
    key = record + str(counts)
    if key in cache: return cache[key]

    if record[0] == '.':
        value = count_options(record[1:], counts)
        cache[key] = value
        return value
    if record[0] == '#':
        if len(counts) == 0 or len(record) < counts[0]:
            value = 0
            cache[key] = value
            return value 
        count = counts[0]
        for i in range(count):
            if record[i] == '.':
                value = 0
                cache[key] = value
                return value 
        if len(record) == count:
            value = count_options(record[count:], counts[1:])
            cache[key] = value
            return value

        if record[count] == '#':
            value = 0
            cache[key] = value
            return value

        value = count_options(record[count+1:], counts[1:])
        cache[key] = value
        return value 
        
    if record[0] == '?':
        dot_options = count_options(record[1:], counts)
        hash_options = count_options('#' + record[1:], counts)
        value = dot_options + hash_options
        cache[key] = value
        return value 
    

assert count_options("???.###", [1,1,3]) == 1
assert count_options(".??..??...?##.", [1,1,3]) == 4
assert count_options("?#?#?#?#?#?#?#?", [1,3,1,6]) == 1
assert count_options('?###????????', [3,2,1]) == 10


def count_all_options(records) -> int:
    sum = 0
    for record in records:
        count = count_options(record[0], record[1])
        sum += count
    return sum

input = read_input2('input.txt')
# input = read_input2('input_small.txt')

res = count_all_options(input)
print(res)

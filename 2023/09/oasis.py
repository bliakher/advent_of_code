def parse_input(file_name) -> list[list[int]]:
    sequences = []
    with open(file_name) as f:
        for line in f.readlines():
            s = parse_num_line(line)
            sequences.append(s)
    return sequences

def parse_num_line(line: str) -> list[int]:
    result = []
    for s in line.split(' '):
        result.append(int(s))
    return result

def get_differences(sequence: list[int]) -> (list[int], bool):
    all_zeros = True
    prev = sequence[0]
    differences = []
    for i in range(1, len(sequence)):
        dif = sequence[i] - prev
        differences.append(dif)
        prev = sequence[i]
        if dif != 0:
            all_zeros = False
    return differences, all_zeros

def get_prediction(sequence: list[int]) -> int:
    seq_ends = []
    seq_ends.append(sequence[-1])
    cur_seq = sequence
    while True:
        diffs, all_zero = get_differences(cur_seq)
        if all_zero:
            break
        seq_ends.append(diffs[-1])
        cur_seq = diffs
    print(seq_ends)
        
    diff_to_next = 0
    for i in range(len(seq_ends) - 1, -1, -1):
        cur = seq_ends[i]
        diff_to_next = diff_to_next + cur
    return diff_to_next

def get_all_predictions(history: list[list[int]]) -> int:
    sum = 0
    for seq in history:
        pred = get_prediction(seq)
        print(pred)
        sum += pred
    return sum


def get_prediction_backwards(sequence: list[int]) -> int:
    seq_ends = []
    seq_ends.append(sequence[0])
    cur_seq = sequence
    while True:
        diffs, all_zero = get_differences(cur_seq)
        if all_zero:
            break
        seq_ends.append(diffs[0])
        cur_seq = diffs
    print(seq_ends)
        
    diff_to_next = 0
    for i in range(len(seq_ends) - 1, -1, -1):
        cur = seq_ends[i]
        diff_to_next = cur - diff_to_next
    return diff_to_next

def get_all_predictions2(history: list[list[int]]) -> int:
    sum = 0
    for seq in history:
        pred = get_prediction_backwards(seq)
        print(pred)
        sum += pred
    return sum


sequences = parse_input('input.txt')
# sequences = parse_input('input_small.txt')

res = get_all_predictions(sequences)
print(res)

print('-----------------------------------')

res2 = get_all_predictions2(sequences)
print(res2)

def parse_input(file_name):
    times = []
    records = []
    with open(file_name) as f:
        lines = f.readlines()
        times = parse_line(lines[0])
        records = parse_line(lines[1])
    return times, records

def parse_line(line: str):
    numbers = line.split(':')[1].strip().split(' ')
    res = []
    for num in numbers:
        if num != '':
            res.append(int(num))
    return res

def count_winning_options(time: int, cur_record: int) -> int:
    speed = 0
    winning = 0
    for i in range(1,time + 1):
        print(i)
        speed += 1
        time_left = time - i
        distance = time_left * speed
        if distance > cur_record:
            winning += 1
    return winning

def count_race(times: list[int], records: list[int]) -> int:
    total_winnings = 1
    for i in range(len(times)):
        wins = count_winning_options(times[i], records[i])
        print('wins', wins)
        total_winnings *= wins
    return total_winnings

# t, r = parse_input('input.txt')
# t, r = parse_input('input_small.txt')

# res = count_race(t, r)
# print(res)

res = count_winning_options(47847467, 207139412091014)
print(res)


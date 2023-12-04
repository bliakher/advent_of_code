import functools 


def read_input(file_name) -> list[list[int]]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            parts = line.split(':')[1].strip().split('|')
            winning = []
            for c in parts[0].strip().split(' '):
                if c != '':
                    winning.append(int(c))
            actual = []
            for c in parts[1].strip().split(' '):
                if c != '':
                    actual.append(int(c))
            result.append(winning)
            result.append(actual)
    return result

def count_points(cards: list[list[int]]) -> int:
    sum = 0
    for i in range(0, len(cards), 2):
        winning = cards[i]
        actual = cards[i + 1]
        win = 0
        for num in actual:
            if num in winning:
                win = 1 if win == 0 else win * 2
        sum += win
    return sum

def count_winning_nums(cards: list[list[int]]):
    win_counts = {}
    for i in range(0, len(cards), 2):
        winning = cards[i]
        actual = cards[i + 1]
        win = 0
        for num in actual:
            if num in winning:
                win += 1
        win_counts[i // 2] = win
    count = len(cards) // 2
    cards_counts: list[int] = [1] * count
    # print(win_counts)
    # print(cards_counts)
    for key in win_counts:
        wins = win_counts[key]
        cur_card_count = cards_counts[key]
        for i in range(wins):
            cards_counts[key + i + 1] += cur_card_count
        # print(cards_counts)
    sum = functools.reduce(lambda a, b: a+b, cards_counts)
    return sum

# input = read_input('input_small.txt')
input = read_input('input.txt')

# res = count_points(input)
# print(res)

res2 = count_winning_nums(input)
print(res2)

            
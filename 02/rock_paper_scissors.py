      
points = {
    'A' : 1,
    'B' : 2,
    'C' : 3
}

result_points = {
    'X' : 0,
    'Y' : 3,
    'Z' : 6
}

shapes = {
    'X' : 'A',
    'Y' : 'B',
    'Z' : 'C'
}

def get_result(oponent, you):
    if oponent == you:
        return 3
    if oponent == 'A':
        if you == 'B':
            return 6
        return 0
    if oponent == 'B':
        if you == 'A':
            return 0
        return 6
    if oponent == 'C':
        if you == 'A':
            return 6
        return 0
        
def get_winning_symbol_points(oponent):
    oponent_points = points[oponent]
    your_points = oponent_points - 1
    return your_points if your_points != 0 else 3

def get_losing_symbol_points(oponent):
    oponent_points = points[oponent]
    your_points = (oponent_points + 1) % 3
    return your_points if your_points != 0 else 3

def get_play_points(oponent, result):
    if result == 'Y':
        return points[oponent]
    if result == 'X':
        return get_winning_symbol_points(oponent)
    if result == 'Z':
        return get_losing_symbol_points(oponent)


def count_tournament_result(file_name):
    total = 0
    with open(file_name) as f:
        for line in f.readlines():
            round = line.strip().split(' ')
            oponent = round[0]
            you = shapes[round[1]]
            win_points = get_result(oponent, you)
            # print("win p ", win_points)
            result = win_points + points[you]
            print(result)
            total += result
    return total

def count_tournament_result2(file_name):
    total = 0
    with open(file_name) as f:
        for line in f.readlines():
            round = line.strip().split(' ')
            oponent = round[0]
            result = round[1]
            points = get_play_points(oponent, result)
            res_points = points + result_points[result]
            # print(result)
            total += res_points
    return total


res = count_tournament_result2('input.txt')
print(res)
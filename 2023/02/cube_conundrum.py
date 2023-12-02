
class Draw:
    def __init__(self, red, green, blue) -> None:
        self.red = red
        self.green = green
        self.blue = blue

    def print(self):
        print(self.red, 'R', self.green, 'G', self.blue, 'B', end=';')
    
    def is_correct(self, max_red: int, max_green: int, max_blue: int) -> bool:
        return self.red <= max_red and self.green <= max_green and self.blue <= max_blue

class Game:
    def __init__(self, id: int, draws: list[Draw]) -> None:
        self.id = id
        self.draws = draws

    def print(self):
        print('Game', self.id, '-', end=' ')
        for draw in self.draws:
            draw.print()
        print()
    
    def is_correct(self, max_red: int, max_green: int, max_blue: int) -> bool:
        correct = True
        for draw in self.draws:
            if not draw.is_correct(max_red, max_green, max_blue):
                correct = False
                break
        return correct
    
    def find_min(self):
        min_red = 0
        min_green = 0
        min_blue = 0
        for draw in self.draws:
            if draw.red > min_red:
                min_red = draw.red
            if draw.green > min_green:
                min_green = draw.green
            if draw.blue > min_blue:
                min_blue = draw.blue
        power = min_red * min_green * min_blue
        # print(power, '-', min_red, 'R', min_green, 'G', min_blue, 'B')
        return power

def parse_draw(str: str) -> Draw :
    parts: list[str] = ''.join(str.split(',')).split(' ')
    red = 0
    green = 0
    blue = 0
    if 'red' in parts:
        idx_red = parts.index('red')
        red = int(parts[idx_red - 1])
    if 'green' in parts:
        idx_grn = parts.index('green')
        green = int(parts[idx_grn - 1])
    if 'blue' in parts:
        idx_blu = parts.index('blue')
        blue = int(parts[idx_blu - 1])
    return Draw(red, green, blue)


def parse_game(line: str) -> Game:
    parts = line.split(':')
    id_part = parts[0]
    id = int(id_part.split(' ')[1])
    draws_part = parts[1].strip()
    draws_list = draws_part.split(';')
    draws = []
    for draw_rec in draws_list:
        draw = parse_draw(draw_rec)
        draws.append(draw)
    return Game(id, draws)

def read_input(file_name) -> list[Game]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            str = line.strip()
            game = parse_game(str)
            result.append(game)
    return result

def check_games(games: list[Game]) -> int:
    sum = 0
    for game in games:
        if game.is_correct(12, 13, 14):
            # print('corr', game.id)
            sum += game.id
    return sum

def find_game_powers(games: list[Game]) -> int:
    sum = 0
    for game in games:
        # print('Game', game.id)
        sum += game.find_min()
    return sum

games = read_input('input.txt')
# games = read_input('small_input.txt')

# for game in games:
#     game.print()

res = check_games(games)
print(res)

res2 = find_game_powers(games)
print(res2)
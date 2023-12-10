class Point:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def print(self):
        print(f"({self.x}, {self.y})")

    def to_string(self) -> str:
        return f"({self.x}, {self.y})"


class Node:
    def __init__(self, symbol: str, position: Point, connected_from: Point, distance: int) -> None:
        self.symbol = symbol
        self.position = position
        self.connected_from = connected_from
        self.distance = distance

    def print(self):
        print('node', self.symbol, self.position.to_string(), 'from:', self.connected_from.to_string(), 'dist:', self.distance)

    def to_string(self):
        return f"node: {self.symbol} {self.position.to_string()} dist: {self.distance}"

    def is_connected(self) -> bool:
        x_diff = self.position.x - self.connected_from.x
        y_diff = self.position.y - self.connected_from.y
        if x_diff == 0:
            if y_diff == 1: # from north v
                return self.symbol in ['|', 'L', 'J']
            elif y_diff == -1: # from south ^
                return self.symbol in ['|', 'F', '7']
            else:
                raise Exception('Impos y_diff', y_diff)
        elif y_diff == 0:
            if x_diff == 1: # from west >
                return self.symbol in ['J', '-', '7']
            elif x_diff == -1: # from east <
                return self.symbol in ['-', 'F', 'L']
            else: 
                raise Exception('Impos x_diff', x_diff)
        else:
            raise Exception(x_diff, y_diff)

    def get_next(self) -> Point:
        x_diff = self.position.x - self.connected_from.x
        y_diff = self.position.y - self.connected_from.y
        next_direction = {}
        if x_diff == 0:
            if y_diff == 1: # from north v
                next_direction = {
                    '|': [0, 1], 
                    'L': [1, 0], 
                    'J': [-1, 0]
                }
            elif y_diff == -1: # from south ^
                next_direction = {
                    '|': [0, -1],
                    'F': [1, 0],
                    '7': [-1, 0]
                }
        elif y_diff == 0:
            if x_diff == 1: # from west >
                next_direction = {
                    'J': [0, -1],
                    '-': [1, 0],
                    '7': [0, 1]
                }
            elif x_diff == -1: # from east <
                next_direction = {
                    '-': [-1, 0],
                    'F': [0, 1],
                    'L': [0, -1]
                }
        direction = next_direction[self.symbol]
        return Point(self.position.x + direction[0], self.position.y + direction[1])

s = ['|', 'L', 'J', 'F', '-', '7']



def read_input(file_name) -> list[list[str]]:
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            row = []
            for c in line:
                row.append(c)
            result.append(row)
    return result

def find_start(maze: list[list[str]]) -> Point:
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if maze[i][j] == 'S':
                return Point(j, i) # switch - x is horizontal
    raise Exception('Start not found')

def get_start_neighbors(start: Point, maze: list[list[str]]) -> list[Node]:
    result = []
    for n in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        x = start.x + n[0]
        y = start.y + n[1]
        symbol = maze[y][x]
        if symbol != '.':
            # print(symbol)
            result.append(Node(symbol, Point(x, y), start, 1))
    return result



def navigate_maze(maze: list[list[str]]) -> int:
    start = find_start(maze)
    start.print()
    # print()
    max_distance = 0
    max_position = Point(-1, -1)
    queue = get_start_neighbors(start, maze)
    visited = set()
    while len(queue) > 0:
        node = queue.pop(0)
        node.print()
        if not node.is_connected():
            print('not connected')
            continue
        next_point = node.get_next()
        symbol = maze[next_point.y][next_point.x]
        next_node = Node(symbol, next_point, node.position, node.distance + 1)
        position_tuple = tuple([next_point.x, next_point.y])
        # print(position_tuple, visited)
        print('next:', next_node.to_string())
        if not (position_tuple in visited):
            print('add to queue')
            queue.append(next_node)
            visited.add(position_tuple)
            if next_node.distance > max_distance:
                max_distance = next_node.distance
                max_position = next_node.position
        
    print(max_distance, max_position.to_string())



maze = read_input('input.txt')

navigate_maze(maze)
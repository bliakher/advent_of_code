
def read_input(file_name):
    res = []
    with open(file_name) as f:
        for line in f.readlines():
            row = []
            for tree in line.strip():
                height = int(tree)
                row.append(height)
            res.append(row)
    return res

def check_if_visible(i, j, grid):
    directions = [ [1, 0], [-1, 0], [0, 1], [0, -1] ]
    my_height = grid[i][j]
    for direction in directions:
        k = i + direction[0]
        l = j + direction[1]
        is_visible = True
        while k >= 0 and k < len(grid) and l >=0 and l < len(grid[0]):
            next_height = grid[k][l]
            if next_height >= my_height:
                is_visible = False
                break
            k += direction[0]
            l += direction[1]
        if is_visible:
            return True
    return False

def count_visible(grid):
    visible = 0
    # borders are visible
    borders = 2 * len(grid) + 2 * len(grid[0]) - 4
    print(borders)
    visible += borders
    # skip borders
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            tree = grid[i][j]
            is_visible = check_if_visible(i, j, grid)
            # print(tree, is_visible, end=', ')
            if is_visible:
                visible += 1

    return visible


def get_scenic_score(i, j, grid):
    directions = [ [1, 0], [-1, 0], [0, 1], [0, -1] ]
    my_height = grid[i][j]
    scenic_score = 1
    for direction in directions:
        k = i + direction[0]
        l = j + direction[1]
        visibility = 0
        while k >= 0 and k < len(grid) and l >=0 and l < len(grid[0]):
            visibility += 1
            next_height = grid[k][l]
            if next_height >= my_height:
                break
            k += direction[0]
            l += direction[1]
        scenic_score *= visibility
    return scenic_score

def count_visible2(grid):
    # skip borders
    max_score = 0
    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[0]) - 1):
            score = get_scenic_score(i, j, grid)
            if score > max_score:
                max_score = score
    return max_score


tree_grid = read_input('/Users/evgeniagolubeva/adventOfCode2022/08/input.txt')
print(count_visible2(tree_grid))
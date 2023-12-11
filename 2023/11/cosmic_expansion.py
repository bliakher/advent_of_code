
def read_input(file_name):
    map = []
    rows_duplicated = []
    cols_duplicated = []
    galaxy_list = []
    with open(file_name) as f:
        idx = 0
        for line in f.readlines():
            row = []
            has_galaxy = False
            for c in line.strip():
                row.append(c)
                if c == '#':
                    has_galaxy = True
            map.append(row)
            if not has_galaxy: # expand by this row
                rows_duplicated.append(idx)
            idx += 1
        for j in range(len(map[0])):
            has_galaxy = False
            for i in range(len(map)):
                row = map[i]
                if row[j] == '#':
                    has_galaxy = True
                    galaxy_list.append([i, j])
            if not has_galaxy:
                cols_duplicated.append(j)
    rows_duplicated.sort()
    cols_duplicated.sort()
    return rows_duplicated, cols_duplicated, galaxy_list

def find_distance(gal1, gal2, duplication, rows_duplicated, cols_duplicated):
    min_y = min(gal1[0], gal2[0])
    max_y = max(gal1[0], gal2[0])
    min_x = min(gal1[1], gal2[1])
    max_x = max(gal1[1], gal2[1])
    y_diff = max_y - min_y
    x_diff = max_x - min_x
    distance = x_diff + y_diff

    for row in rows_duplicated:
        if row <= min_y:
            continue
        if row < max_y:
            distance += duplication - 1
        else:
            break
    for col in cols_duplicated:
        if col <= min_x:
            continue
        if col < max_x:
            distance += duplication - 1
        else:
            break
    return distance

def find_distances_to_the_rest(galaxies, gal_idx, duplication, rows_duplicated, cols_duplicated):
    total = 0
    cur_galaxy = galaxies[gal_idx]
    for i in range(len(galaxies)):
        if i != gal_idx:
            dist = find_distance(cur_galaxy, galaxies[i], duplication, rows_duplicated, cols_duplicated)
            total += dist
    return total

def find_all_distances(galaxies, duplication, rows_duplicated, cols_duplicated):
    total = 0
    for i in range(len(galaxies)):
        dist = find_distances_to_the_rest(galaxies, i, duplication, rows_duplicated, cols_duplicated)
        total += dist
    return total
    

rows_duplicated, cols_duplicated, galaxy_list = read_input('input.txt')
# rows_duplicated, cols_duplicated, galaxy_list = read_input('input_small.txt')

res1 = find_all_distances(galaxy_list, 2, rows_duplicated, cols_duplicated)
print('res1', res1 // 2)

res2 = find_all_distances(galaxy_list, 1000000, rows_duplicated, cols_duplicated)
print('res2', res2 // 2)



class Map:
    def __init__(self, fr: list[int], to: list[int]) -> None:
        self.fr = fr
        self .to = to

    def print(self):
        print('fr', self.fr)
        print('to', self.to)


def create_range_from_map(map_lines: list[list[int]]):
    # sort by the source range start
    map_lines.sort(key=lambda x: x[1])
    fr = []
    to = []
    for idx in range(len(map_lines)):
        cur = map_lines[idx]
        # map doesn't start with zero - map zero to zero
        if idx == 0 and cur[1] != 0:
            fr.append(0)
            to.append(0)

        fr.append(cur[1])
        to.append(cur[0])

        # fill in the end
        if idx == len(map_lines) - 1:
            fr.append(cur[1] + cur[2])
            to.append(cur[1] + cur[2])
    print(fr, to)
    return fr, to

def parse_num_line(line: str) -> list[int]:
    result = []
    for s in line.split(' '):
        result.append(int(s))
    return result

def parse_input(file_name) -> (list[int], list[Map]):
    seeds = []
    read_seeds = False
    second = False
    reading_map = False
    cur_map = []
    maps = []
    with open(file_name) as f:
        for line in f.readlines():
            line = line.strip()
            if not read_seeds:
                read_seeds = True
                seeds = parse_num_line(line.split(':')[1].strip())
                continue
            
            if not second:
                second = True
                continue

            if line == '' and len(cur_map) != 0:
                fr, to = create_range_from_map(cur_map)
                maps.append(Map(fr, to))
                cur_map = []
                reading_map = False
                continue

            if not line[0].isdigit() :
                reading_map = True
                # print('start map', line)
                continue

            if reading_map:
                if not line[0].isdigit():
                    print('error', line)
                cur_map.append(parse_num_line(line))
    if len(cur_map) != 0:
        fr, to = create_range_from_map(cur_map)
        maps.append(Map(fr, to))
    return seeds, maps

def find_closest_smallest(value: int, starts: list[int]):
    for i in range(len(starts)):
        if i == len(starts) - 1:
            return i
        cur = starts[i]
        next = starts[i+1]
        if value >= cur and value < next:
            return i
    return -1


def map_seed_to_location(seed: int, map_list: list[Map]) -> int:
    cur = seed
    for map in map_list:
        mapping_idx = find_closest_smallest(cur, map.fr)
        print('closest sm', map.fr[mapping_idx])
        diff = cur - map.fr[mapping_idx] # difference from the closest range point
        cur = map.to[mapping_idx] + diff
        print('mapping to:', cur)

    return cur


def find_min_location(seeds: list[int], map_list: list[Map]):
    locations = []
    for seed in seeds:
        print('seed:', seed)
        loc = map_seed_to_location(seed, map_list)
        print('loc', loc)
        locations.append(loc)
    print(locations)
    return min(locations)


seeds, maps = parse_input('input_small.txt')
# seeds, maps = parse_input('input.txt')

print(seeds)
for map in maps:
    map.print()
    print()

res = find_min_location(seeds, maps)
print(res)


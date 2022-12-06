
class Section:
    def __init__(self, start, end):
        self.start = start
        self.end = end

def parse_section(str):
    ends = str.split('-')
    start = int(ends[0])
    end = int(ends[1])
    return Section(start, end)

def read_input(file_name):
    res = []
    with open(file_name) as f:
        for line in f.readlines():
            pair = line.strip().split(',')
            section1 = parse_section(pair[0])
            section2 = parse_section(pair[1])
            res.append([section1, section2])
    return res

def is_contained(section1, section2):
    if section1.start == section2.start or section1.end == section2.end:
        return True
    min_section = section1 if section1.start < section2.start else section2
    max_section = section1 if section1.start > section2.start else section2
    return min_section.end >= max_section.end

def has_overlap(section1, section2):
    if section1.start == section2.start or section1.end == section2.end:
        return True
    min_section = section1 if section1.start < section2.start else section2
    max_section = section1 if section1.start > section2.start else section2
    return min_section.end >= max_section.start

def find_fully_contained(file_name):
    counter = 0
    input = read_input(file_name)
    for pair in input:
        section1 = pair[0]
        section2 = pair[1]
        contained = is_contained(section1, section2)
        # print([section1.start, section1.end],[section2.start, section2.end], contained)
        if contained:
            counter += 1
    return counter

def find_overlaped(file_name):
    counter = 0
    input = read_input(file_name)
    for pair in input:
        section1 = pair[0]
        section2 = pair[1]
        overlap = has_overlap(section1, section2)
        # print([section1.start, section1.end],[section2.start, section2.end], contained)
        if overlap:
            counter += 1
    return counter

# res = find_fully_contained('test_input.txt')
res = find_overlaped('input.txt')
print(res)




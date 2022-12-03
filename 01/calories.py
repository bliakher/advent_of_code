def find_max_calories(file_name):
    max = 0
    sum = 0
    with open(file_name) as f:
        for line in f.readlines():
            str = line.strip()
            if str == "":
                if sum > max:
                    max = sum
                sum = 0
            else:
                num = int(str)
                sum += num
    return max

def find_top_3_calories(file_name):
    calories = []
    sum = 0
    with open(file_name) as f:
        for line in f.readlines():
            str = line.strip()
            if str == "":
                calories.append(sum)
                sum = 0
            else:
                num = int(str)
                sum += num
    calories.sort(reverse=True)
    return calories[0] + calories[1] + calories[2]

# res = find_max_calories('./input.txt')

res = find_top_3_calories('input.txt')
print(res)
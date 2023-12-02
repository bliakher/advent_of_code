
def read_input(file_name):
    result = []
    with open(file_name) as f:
        for line in f.readlines():
            str = line.strip()
            result.append(str)
    return result


def read_calibration(calibration_list):
    sum = 0
    for line in calibration_list:
        first_dig = 0
        last_dig = 0
        first = False
        for c in line:
            if c.isdigit():
                i = int(c)
                if not first:
                    first_dig = i
                    first = True
                last_dig = i
        cal_value = first_dig * 10 + last_dig
        sum += cal_value
    return sum

digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

def read_calibration2(calibration_list):
    sum = 0
    for line in calibration_list:
        first_dig = 0
        last_dig = 0
        first = False
        read_digit = False
        cur_text = ''
        i = 0
        for c in line:
            if c.isdigit():
                i = int(c)
                read_digit = True
            else:
                cur_text += c
                if cur_text in digits:
                    i = digits.index(cur_text) + 1
                    read_digit = True
                    cur_text = ''

            if read_digit:
                print(i)
                if not first:
                    first_dig = i
                    first = True
                last_dig = i
                read_digit = False      
        cal_value = first_dig * 10 + last_dig
        sum += cal_value
        print()
        print(cal_value, sum)
        print()
    return sum

def read_calibration3(calibration_list):
    sum = 0
    for line in calibration_list:
        digit_dict = find_digits(line)
        min_pos = min(digit_dict.keys())
        max_pos = max(digit_dict.keys())
        first_dig = digit_dict[min_pos]
        last_dig = digit_dict[max_pos]
        cal_value = first_dig * 10 + last_dig
        print(digit_dict)
        print(first_dig, last_dig, cal_value)
        sum += cal_value
    return sum

def find_digits(line):
    digit_dic = {}
    for order in range(len(digits)):
        text_digit = digits[order]
        pos = line.find(text_digit)
        start = pos
        while pos != -1:
            digit_dic[pos] = order + 1
            start += len(text_digit)
            pos = line.find(text_digit, start)
    for pos in range(len(line)):
        c = line[pos]
        if c.isdigit():
            i = int(c)
            digit_dic[pos] = i
    return digit_dic


input = read_input('./input.txt')

input_small = read_input('./input_small.txt')
# print(read_calibration(input))

# print(read_calibration2(input))
# print(read_calibration3(input_small))
print(read_calibration3(input))
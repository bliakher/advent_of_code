import math

def count_reach_zero(filename):
    cur_dial = 50
    zero_count = 0
    with open(filename) as f:
        for line in f.readlines():
            # stripped = line.strip()
            direction = 1 if line[0] == 'R' else -1
            steps = int(line[1:])
            move = direction * steps
            cur_dial = (cur_dial + move + 100) % 100
            if cur_dial == 0:
                zero_count += 1
    return zero_count

def count_pass_zero(filename):
    cur_dial = 50
    zero_count = 0
    with open(filename) as f:
        for line in f.readlines():
            direction = 1 if line[0] == 'R' else -1
            steps = int(line[1:])
            move = direction * steps
            target = cur_dial + move
            if target >= 100 or target <= 0:
                passes = steps // 100
                if cur_dial != 0 or passes > 0:
                    passes += 1
                zero_count += passes
            cur_dial = (cur_dial + move + 100) % 100
    return zero_count

def count_pass_zero(filename):
    cur_dial = 50
    zero_count = 0
    with open(filename) as f:
        for line in f.readlines():
            direction = 1 if line[0] == 'R' else -1
            steps = int(line[1:])
            passes = steps // 100
            steps = steps - passes * 100
            move = direction * steps
            target = cur_dial + move

            if (target <= 0 or target >= 100) and cur_dial != 0:
                passes += 1

            cur_dial = target % 100
            zero_count += passes
    return zero_count


print('part 1:', count_reach_zero('input.txt'))
print('part 2:', count_pass_zero('input.txt'))

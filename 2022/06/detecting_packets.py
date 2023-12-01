
def detect_packet_marker(stream):
    start = 0
    window = set()
    detected = False
    while not detected:
        for i in range(4):
            next_char = stream[start + i]
            # print(next_char, end='')
            if next_char in window:
                window = set()
                break
            else:
                window.add(next_char)
                if i == 3:
                    detected = True
        start += 1
        # print()
    return start + 3


def detect_packet_marker2(stream):
    start = 0
    window = set()
    detected = False
    while not detected:
        for i in range(14):
            next_char = stream[start + i]
            # print(next_char, end='')
            if next_char in window:
                window = set()
                break
            else:
                window.add(next_char)
                if i == 13:
                    detected = True
        start += 1
        # print()
    return start + 13



with open('input.txt') as f:
    stream = f.readline().strip()
    res = detect_packet_marker2(stream)
    print(res)
    print(detect_packet_marker2('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg'))

            


# def detect_packet_marker(stream):
#     start = 0
#     end = 1
#     window = set([stream[0]])
#     char_ofsets = {
#         stream[0]: 1
#     }
#     detected = False
#     while not detected:
#         next_char = stream[end]
#         if next_char in window:
#             duplicate_ofset = char_ofsets[next_char]
#             start += duplicate_ofset
#             char_ofsets[next_char] = 
#         else:
#             window.add(next_char)
#             char_ofsets[next_char] = len(window)
#             if len(window) == 4:
#                 detected = True
#                 break
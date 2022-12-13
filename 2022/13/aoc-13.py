import json


FILE_PATH = "./input.txt"


def parse_input():
    pairs = []
    packet_1 = None
    packet_2 = None
    i = 0
    with (open(FILE_PATH)) as input_file:
        for line in input_file:
            if i % 3 == 0:
                packet_1 = json.loads(line.strip())
            elif i % 3 == 1:
                packet_2 = json.loads(line.strip())
            elif i % 3 == 2:
                pairs.append((packet_1, packet_2))
                packet_1 = None
                packet_2 = None
            i += 1
    pairs.append((packet_1, packet_2))

    return pairs


def parse_input_2():
    packets = []
    with (open(FILE_PATH)) as input_file:
        for line in input_file:
            if len(line.strip()) == 0:
                continue
            packets.append(json.loads(line.strip()))
    return packets


def compare_pair(left, right):
    if len(left) == 0:
        return True

    i = 0
    left_len = len(left)
    right_len = len(right)
    length = left_len if left_len > right_len else right_len
    while i < length:
        if i >= right_len:  # ran out of right
            return False
        if i >= left_len:  # ran out of left
            return True

        left_item = left[i]
        right_item = right[i]

        if type(left_item) == list or type(right_item) == list:
            new_left = left_item if type(left_item) == list else [left_item]
            new_right = right_item if type(
                right_item) == list else [right_item]
            comparison = compare_pair(new_left, new_right)
            if comparison is None:
                i += 1
                continue
            else:
                return comparison
        else:  # both numbers
            if left_item == right_item:
                i += 1
                continue
            else:
                return left_item < right_item

    return None


def part_1(pairs):
    correct_pairs = []
    for i in range(len(pairs)):
        pair = pairs[i]
        left = pair[0]
        right = pair[1]
        comparison = compare_pair(left, right)
        if comparison is None or comparison:
            correct_pairs.append(i+1)

    return sum(correct_pairs)


def cmp_packets(packet_1, packet_2):
    comparison = compare_pair(packet_1, packet_2)
    return -1 if comparison else 1


def part_2(packets):
    packets.sort(cmp_packets)
    divider_1_index = packets.index([[2]]) + 1
    divider_2_index = packets.index([[6]]) + 1
    return divider_1_index * divider_2_index


if __name__ == "__main__":
    pairs = parse_input()
    result_1 = part_1(pairs)
    print("Part 1: ", result_1)

    packets = parse_input_2()
    packets.append([[2]])
    packets.append([[6]])
    result_2 = part_2(packets)
    print("Part 2: ", result_2)

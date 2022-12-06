def parse_input():
    input = ""
    with (open("./input.txt")) as input_file:
        for line in input_file:
            input += line.strip()

    return input


def part_1(input):
    buffer = set()
    for i in range(len(input)):
        buffer.add(input[i])
        if i >= 3:
            if len(buffer) >= 4:
                return i + 1
            buffer = set()
            buffer.add(input[i])
            buffer.add(input[i-1])
            buffer.add(input[i-2])

    return len(input)


def part_2(input):
    buffer = set()
    for i in range(len(input)):
        buffer.add(input[i])
        if i >= 13:
            if len(buffer) >= 14:
                return i + 1
            buffer = set()
            for j in range(i, i-13, -1):
                buffer.add(input[j])

    return len(input)


if __name__ == "__main__":
    input = parse_input()
    result_1 = part_1(input)
    print("Part 1: ", result_1)
    result_2 = part_2(input)
    print("Part 2: ", result_2)

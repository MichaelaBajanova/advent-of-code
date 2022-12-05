def parse_input():
    lines = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            lines.append(line.strip())

    return lines


def part_1(lines):
    result = 0
    return result


def part_2(lines):
    result = 0
    return result


if __name__ == "__main__":
    lines = parse_input()
    result_1 = part_1(lines)
    print("Part 1: ", result_1)
    result_2 = part_2(lines)
    print("Part 2: ", result_2)

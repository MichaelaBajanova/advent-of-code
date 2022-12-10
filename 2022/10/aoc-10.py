class Instruction:
    def __init__(self, type, value):
        self.type = type
        self.value = value


def parse_input():
    instructions = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.strip().split()
            type = line_split[0]
            value = None if len(line_split) == 1 else int(line_split[1])
            instructions.append(Instruction(type, value))

    return instructions


def part_1(instructions):
    x = 1
    cycle = 1
    CYCLE_VALUES_TO_CHECK = [20, 60, 100, 140, 180, 220]
    strengths = {"20": None, "60": None, "100": None,
                 "140": None, "180": None, "220": None}
    for instruction in instructions:
        if instruction.type == "noop":
            if cycle in CYCLE_VALUES_TO_CHECK:
                strengths[str(cycle)] = x
            cycle += 1

        if instruction.type == "addx":
            if cycle in CYCLE_VALUES_TO_CHECK:
                strengths[str(cycle)] = x
            cycle += 1
            if cycle in CYCLE_VALUES_TO_CHECK:
                strengths[str(cycle)] = x
            cycle += 1
            x += instruction.value

    result = 0
    for cycle in strengths:
        result += int(cycle) * strengths[cycle]

    return result


def print_crt(crt):
    for y in range(6):
        for x in range(40):
            print(crt[y][x], end="")
        print()


def draw_pixel(crt, x, cycle):
    sprite = [x-1, x, x+1]
    if (cycle % 40 - 1) in sprite:
        xx = cycle % 40 - 1
        yy = cycle // 40
        crt[yy][xx] = '#'
    return crt


def part_2(instructions):
    crt = []
    # init crt
    for y in range(6):
        crt.append([])
        for x in range(40):
            crt[y].append('.')

    x = 1
    cycle = 1
    for instruction in instructions:
        if instruction.type == "noop":
            crt = draw_pixel(crt, x, cycle)
            cycle += 1

        if instruction.type == "addx":
            crt = draw_pixel(crt, x, cycle)
            cycle += 1
            crt = draw_pixel(crt, x, cycle)
            cycle += 1
            x += instruction.value

    print_crt(crt)


if __name__ == "__main__":
    instructions = parse_input()
    result_1 = part_1(instructions)
    print("Part 1: ", result_1)
    part_2(instructions)

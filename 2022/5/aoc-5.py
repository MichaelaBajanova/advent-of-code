class Instruction:
    def __init__(self, count, frm, to):
        self.count = count
        self.frm = frm
        self.to = to


def parse_input():
    stacks = []
    instructions = []
    is_reading_instructions = False
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            if len(line_strip) == 0:
                is_reading_instructions = True
                continue
            if not is_reading_instructions:
                current_top_crates = line_strip.split()
                if len(stacks) == 0:
                    for _ in current_top_crates:
                        stacks.append([])
                for i in range(len(current_top_crates)):
                    crate = current_top_crates[i]
                    if crate != "[_]" and crate[0] == '[':
                        stacks[i].insert(0, crate)
            else:
                line_split = line_strip.split()
                count = int(line_split[1])
                frm = int(line_split[3]) - 1
                to = int(line_split[5]) - 1
                instructions.append(Instruction(count, frm, to))

    return {"stacks": stacks, "instructions": instructions}


def move_crates(stacks, instruction):
    for _ in range(instruction.count):
        crate_to_move = stacks[instruction.frm].pop()
        stacks[instruction.to].append(crate_to_move)
    return stacks


# now we can move multiple crates at once
def move_crates_2(stacks, instruction):
    crates_to_move = []
    print()
    for stack in stacks:
        print(stack)
    print()
    for _ in range(instruction.count):
        crates_to_move.append(stacks[instruction.frm].pop())
    crates_to_move.reverse()
    stacks[instruction.to] += crates_to_move
    return stacks


def part_1(stacks, instructions):
    result = ""

    current_stacks = [*stacks]
    for instruction in instructions:
        current_stacks = move_crates(current_stacks, instruction)

    for i in range(len(current_stacks)):
        result += current_stacks[i][-1]

    return result.replace('[', '').replace(']', '')


def part_2(stacks, instructions):
    result = ""

    current_stacks = [*stacks]
    for instruction in instructions:
        current_stacks = move_crates_2(current_stacks, instruction)

    for i in range(len(current_stacks)):
        result += current_stacks[i][-1]

    return result.replace('[', '').replace(']', '')


if __name__ == "__main__":
    parsed = parse_input()
    stacks = parsed["stacks"]
    instructions = parsed["instructions"]

    result_1 = part_1(stacks.copy(), instructions)
    print("Part 1: ", result_1)

    parsed = parse_input()
    # hack to get fresh stacks, because they somehow got modified
    stacks_2 = parsed["stacks"]
    result_2 = part_2(stacks_2, instructions)
    print("Part 2: ", result_2)

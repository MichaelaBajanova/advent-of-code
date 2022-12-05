def parse_input():
    sections = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            elves = line.strip().split(",")
            tmp = []
            for elf in elves:
                section = elf.split("-")
                tmp.append((int(section[0]), int(section[1])))
            sections.append(tmp)

    return sections


def is_contained(elf_1, elf_2):
    return elf_1[0] >= elf_2[0] and elf_1[1] <= elf_2[1]


def overlaps(elf_1, elf_2):
    range_1 = range(elf_1[0], elf_1[1]+1)
    range_2 = range(elf_2[0], elf_2[1]+1)
    overlapping = set(range_1).intersection(range_2)
    return len(overlapping) > 0


def part_1(sections):
    result = 0
    for section in sections:
        elf_1 = section[0]
        elf_2 = section[1]
        if is_contained(elf_1, elf_2) or is_contained(elf_2, elf_1):
            result += 1

    return result


def part_2(sections):
    result = 0
    for section in sections:
        elf_1 = section[0]
        elf_2 = section[1]
        if overlaps(elf_1, elf_2):
            result += 1

    return result


if __name__ == "__main__":
    sections = parse_input()
    result_1 = part_1(sections)
    print("Part 1: ", result_1)
    result_2 = part_2(sections)
    print("Part 2: ", result_2)

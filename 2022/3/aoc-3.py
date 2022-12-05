def get_rucksacks():
    rucksacks = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            rucksacks.append(line.strip())

    return rucksacks


def part_1(rucksacks):
    result = 0
    for rucksack in rucksacks:
        half = len(rucksack) // 2
        first_compartment = rucksack[:half]
        second_compartment = rucksack[half:]
        matching = ''.join(
            set(first_compartment).intersection(second_compartment))
        to_substract = 0
        if matching.isupper():
            to_substract = 38
        else:
            to_substract = 96
        result += ord(matching) - to_substract

    return result


def part_2(rucksacks):
    result = 0
    for i in range(len(rucksacks)):
        if i % 3 != 0:
            continue
        matching = ''.join(
            set(rucksacks[i]).intersection(rucksacks[i+1]).intersection(rucksacks[i+2]))
        to_substract = 0
        if matching.isupper():
            to_substract = 38
        else:
            to_substract = 96
        result += ord(matching) - to_substract

    return result


if __name__ == "__main__":
    rucksacks = get_rucksacks()
    result_1 = part_1(rucksacks)
    print("Part 1: ", result_1)
    result_2 = part_2(rucksacks)
    print("Part 2: ", result_2)

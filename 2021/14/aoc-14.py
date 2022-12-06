import math


class Insertion:
    def __init__(self, to, what):
        self.to = to
        self.what = what


def parse_input():
    rules = []
    with (open("./input.txt")) as input_file:
        template = input_file.readline().strip()
        input_file.readline()
        for line in input_file:
            line_split = line.strip().split(" -> ")
            rules.append(Insertion(to=line_split[0], what=line_split[1]))

    return {"template": template, "rules": rules}


def part_1(rules, pairs, num_of_steps):
    current_pairs = pairs.copy()
    for i in range(num_of_steps):
        temp_pairs = current_pairs.copy()
        for rule in rules:
            temp_pairs[rule.to] -= current_pairs[rule.to]
            temp_pairs[rule.to[0]+rule.what] += current_pairs[rule.to]
            temp_pairs[rule.what+rule.to[1]] += current_pairs[rule.to]
        current_pairs = temp_pairs

    # count each char
    char_counts = {}
    for pair in current_pairs:
        char_1 = pair[0]
        char_2 = pair[1]
        if char_1 not in char_counts:
            char_counts[char_1] = 0
        if char_2 not in char_counts:
            char_counts[char_2] = 0

        char_counts[char_1] += current_pairs[pair]
        char_counts[char_2] += current_pairs[pair]

    max = 0
    first_key = next(iter(char_counts))
    min = char_counts[first_key]
    for char in char_counts:
        if char_counts[char] > max:
            max = char_counts[char]
        if char_counts[char] < min:
            min = char_counts[char]

    return math.ceil((max - min) / 2)


def part_2(rules, pairs):
    return part_1(rules, pairs, num_of_steps=40)


if __name__ == "__main__":
    parsed = parse_input()
    template = parsed["template"]
    rules = parsed["rules"]

    pairs = {}
    for rule in rules:
        pairs[rule.to] = 0
    for i in range(len(template)-1):
        current_pair = template[i] + template[i+1]
        pairs[current_pair] += 1

    result_1 = part_1(rules, pairs, 10)
    print("Part 1: ", result_1)
    result_2 = part_2(rules, pairs)
    print("Part 2: ", result_2)

def parse_input():
    lines = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            lines.append(line.strip())

    return lines


OPENING_PARS = ['(', '[', '{', '<']
CLOSING_PARS = [')', ']', '}', '>']
MATCHES = {"(": ')', "[": ']', "{": '}', "<": '>'}


def are_pars_matching(opening, closing):
    return MATCHES[opening] == closing


def get_corrupted_score(line):
    POINTS = {")": 3, "]": 57, "}": 1197, ">": 25137}
    opening = []
    for par in line:
        if par in OPENING_PARS:
            opening.append(par)
        if par in CLOSING_PARS:
            last_opening = opening.pop()
            if not are_pars_matching(last_opening, par):
                return POINTS[par]

    return 0


def part_1(lines):
    score = 0
    for line in lines:
        score += get_corrupted_score(line)

    return score


def get_incomplete_score(line):
    POINTS = {")": 1, "]": 2, "}": 3, ">": 4}
    score = 0
    opening = []
    for par in line:
        if par in OPENING_PARS:
            opening.append(par)
        if par in CLOSING_PARS:
            opening.pop()

    opening.reverse()
    closing = []
    for par in opening:
        closing.append(MATCHES[par])
    for par in closing:
        score = score * 5 + POINTS[par]

    return score


def part_2(lines):
    scores = []
    for line in lines:
        if get_corrupted_score(line) == 0:
            scores.append(get_incomplete_score(line))

    index = len(scores) // 2
    scores.sort()
    return scores[index]


if __name__ == "__main__":
    lines = parse_input()
    result_1 = part_1(lines)
    print("Part 1 (score): ", result_1)
    result_2 = part_2(lines)
    print("Part 2 (middle score): ", result_2)

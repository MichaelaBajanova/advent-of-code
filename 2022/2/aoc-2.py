def get_rounds():
    rounds = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.split()
            opponent = line_split[0]
            me = line_split[1]
            rounds.append((opponent, me))

    return rounds


def is_win(round):
    opponent = round[0]
    me = round[1]
    if opponent == 'A' and me == 'Y':
        return True
    if opponent == 'B' and me == 'Z':
        return True
    if opponent == 'C' and me == 'X':
        return True

    return False


def is_draw(round):
    opponent = round[0]
    me = round[1]
    if opponent == 'A' and me == 'X':
        return True
    if opponent == 'B' and me == 'Y':
        return True
    if opponent == 'C' and me == 'Z':
        return True

    return False


def get_score(round):
    opponent = round[0]
    me = round[1]
    score = 0
    if me == 'X':
        score += 1
    elif me == 'Y':
        score += 2
    elif me == 'Z':
        score += 3

    if is_win(round):
        score += 6
    elif is_draw(round):
        score += 3

    return score


def part_1(rounds):
    score = 0
    for round in rounds:
        score += get_score(round)

    return score


def get_my_shape(round):
    opponent = round[0]
    result = round[1]
    if result == 'Y':
        if opponent == 'A':
            return 'X'
        if opponent == 'B':
            return 'Y'
        if opponent == 'C':
            return 'Z'
    elif result == 'X':
        if opponent == 'A':
            return 'Z'
        if opponent == 'B':
            return 'X'
        if opponent == 'C':
            return 'Y'
    elif result == 'Z':
        if opponent == 'A':
            return 'Y'
        if opponent == 'B':
            return 'Z'
        if opponent == 'C':
            return 'X'


def part_2(rounds):
    score = 0
    for round in rounds:
        print((round[0], get_my_shape(round)))
        score += get_score((round[0], get_my_shape(round)))
    return score


if __name__ == "__main__":
    rounds = get_rounds()
    score = part_1(rounds)
    print("Part 1 score: ", score)
    score_2 = part_2(rounds)
    print("Part 2 score: ", score_2)

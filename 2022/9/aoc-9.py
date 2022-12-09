class Move:
    def __init__(self, direction, count):
        self.direction = direction
        self.count = count


def parse_input():
    moves = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            direction = line.strip().split()[0]
            count = int(line.strip().split()[1])
            moves.append(Move(direction, count))

    return moves


def move_to(direction, coords):
    x = coords[0]
    y = coords[1]
    if direction == 'U':
        return (x, y-1)
    elif direction == 'R':
        return (x+1, y)
    elif direction == 'D':
        return (x, y+1)
    elif direction == 'L':
        return (x-1, y)


def move_tail_to_head(head, tail):
    head_x = head[0]
    head_y = head[1]
    tail_x = tail[0]
    tail_y = tail[1]

    # touching
    if abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) <= 1:
        return tail

    # head moved on x axis
    if abs(head_x - tail_x) > 1 and abs(head_y - tail_y) <= 1:
        # head moved right
        if head_x > tail_x:
            return (tail_x+1, head_y)
        # head moved left
        elif head_x < tail_x:
            return (tail_x-1, head_y)

    # head moved on y axis
    if abs(head_x - tail_x) <= 1 and abs(head_y - tail_y) > 1:
        # head moved down
        if head_y > tail_y:
            return (head_x, tail_y+1)
        # head moved up
        if head_y < tail_y:
            return (head_x, tail_y-1)

    # head moved diagonally
    if abs(head_x - tail_x) > 1 and abs(head_y - tail_y) > 1:
        new_x = head_x - 1 if head_x > tail_x else head_x + 1
        new_y = head_y - 1 if head_y > tail_y else head_y + 1
        return (new_x, new_y)


def part_1(moves):
    start = (0, 0)
    head = start
    tail = start
    tail_positions = set()
    tail_positions.add(tail)
    for move in moves:
        for _ in range(move.count):
            head = move_to(move.direction, head)
            tail = move_tail_to_head(head, tail)
            tail_positions.add(tail)

    return len(tail_positions)


def part_2(moves):
    start = (0, 0)
    knots = {}
    for i in range(10):
        knots[str(i)] = start

    tail_positions = set()
    tail_positions.add(knots["9"])
    for move in moves:
        for _ in range(move.count):
            knots["0"] = move_to(move.direction, knots["0"])
            for i in range(1, 10):
                knot = str(i)
                knots[knot] = move_tail_to_head(knots[str(i-1)], knots[knot])
            tail_positions.add(knots["9"])

    return len(tail_positions)


if __name__ == "__main__":
    moves = parse_input()
    result_1 = part_1(moves)
    print("Part 1: ", result_1)
    result_2 = part_2(moves)
    print("Part 2: ", result_2)

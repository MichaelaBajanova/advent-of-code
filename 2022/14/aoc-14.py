X = 0
Y = 1


def parse_input():
    lines = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            points = line_strip.split(" -> ")
            item_points = []
            for point in points:
                point_split = point.split(',')
                item_points.append((int(point_split[0]), int(point_split[1])))
            lines.append(item_points)

    return lines


def get_max_cave_size(lines):
    max_x = 0
    max_y = 0
    for line in lines:
        for point in line:
            x = point[X]
            if x > max_x:
                max_x = x

            y = point[Y]
            if y > max_y:
                max_y = y

    return (max_x + 1, max_y + 1)


def init_cave(size):
    width = size[X]
    height = size[Y]
    cave = []
    for y in range(height):
        row = []
        for x in range(width):
            row.append('.')
        cave.append(row)
    return cave


def get_cave(lines):
    size = get_max_cave_size(lines)
    cave = init_cave(size)

    for line in lines:
        for i in range(1, len(line)):
            this_point = line[i]
            prev_point = line[i-1]

            dir = Y if this_point[X] == prev_point[X] else X
            frm = min(this_point[dir], prev_point[dir])
            to = max(this_point[dir], prev_point[dir])
            if dir == X:
                for x in range(frm, to+1):
                    cave[prev_point[Y]][x] = '#'
            elif dir == Y:
                for y in range(frm, to+1):
                    cave[y][prev_point[X]] = '#'

    return cave


def place_sand(cave):
    FRM = (500, 0)
    new_pos = (FRM[X], FRM[Y])
    can_move = True
    while can_move:
        if new_pos[Y] >= len(cave)-1 or new_pos[X] < 0 or new_pos[X] >= len(cave[0])-1:
            return None
        while cave[new_pos[Y]+1][new_pos[X]] == '.':
            new_pos = (new_pos[X], new_pos[Y]+1)
        if cave[new_pos[Y]+1][new_pos[X]-1] == '.':  # down left
            new_pos = (new_pos[X]-1, new_pos[Y]+1)
            continue
        if cave[new_pos[Y]+1][new_pos[X]+1] == '.':  # down right
            new_pos = (new_pos[X]+1, new_pos[Y]+1)
            continue

        can_move = False

    return new_pos


def part_1(lines):
    cave = get_cave(lines)
    can_place_sand = True
    sand_count = 0
    while can_place_sand:
        sand_pos = place_sand(cave)
        if sand_pos is None:
            can_place_sand = False
            break

        cave[sand_pos[Y]][sand_pos[X]] = 'o'
        sand_count += 1

    return sand_count


def get_infinite_cave(lines):
    size = get_max_cave_size(lines)
    width = size[X]
    height = size[Y] + 2
    cave = init_cave((width, height))

    for line in lines:
        for i in range(1, len(line)):
            this_point = line[i]
            prev_point = line[i-1]

            dir = Y if this_point[X] == prev_point[X] else X
            frm = min(this_point[dir], prev_point[dir])
            to = max(this_point[dir], prev_point[dir])
            if dir == X:
                for x in range(frm, to+1):
                    cave[prev_point[Y]][x] = '#'
            elif dir == Y:
                for y in range(frm, to+1):
                    cave[y][prev_point[X]] = '#'

    for x in range(width):
        cave[height-1][x] = '#'

    return cave


def place_sand_2(cave):
    FRM = (500, 0)
    width = len(cave[0])
    new_pos = (FRM[X], FRM[Y])
    can_move = True
    while can_move:
        if new_pos[X+1] >= width:
            return new_pos
        while cave[new_pos[Y]+1][new_pos[X]] == '.':
            new_pos = (new_pos[X], new_pos[Y]+1)
        if cave[new_pos[Y]+1][new_pos[X]-1] == '.':  # down left
            new_pos = (new_pos[X]-1, new_pos[Y]+1)
            continue
        if cave[new_pos[Y]+1][new_pos[X]+1] == '.':  # down right
            new_pos = (new_pos[X]+1, new_pos[Y]+1)
            continue

        can_move = False

    return new_pos


def add_cave_column(cave):
    width = len(cave[0])
    height = len(cave)
    for y in range(height):
        cave[y].append('.')

    cave[height-1][width] = '#'
    return cave


def transpose_matrix(matrix):
    result = []
    for _ in range(len(matrix[0])):
        result.append([])

    for row in matrix:
        for i in range(len(row)):
            result[i].append(row[i])

    return result


def print_cave(cave):
    transposed = transpose_matrix(cave[:len(cave)-1])
    frm = 0
    while 'o' not in transposed[frm] and '#' not in transposed[frm]:
        frm += 1
    to = len(transposed)-1
    while 'o' not in transposed[to] and '#' not in transposed[to]:
        to -= 1

    for y in range(len(cave)):
        for x in range(frm, to+1):
            print(cave[y][x], end="")
        print()


def part_2(lines):
    cave = get_infinite_cave(lines)
    # should be enough
    for _ in range(300):
        cave = add_cave_column(cave)
    can_place_sand = True
    sand_count = 0
    while can_place_sand:
        sand_pos = place_sand_2(cave)
        cave[sand_pos[Y]][sand_pos[X]] = 'o'
        sand_count += 1

        if sand_pos == (500, 0):
            can_place_sand = False
            break

    return sand_count


if __name__ == "__main__":
    lines = parse_input()

    result_1 = part_1(lines)
    print("Part 1: ", result_1)
    result_2 = part_2(lines)
    print("Part 2: ", result_2)

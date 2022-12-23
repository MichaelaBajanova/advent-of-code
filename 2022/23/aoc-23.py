import math

X = 0
Y = 1

NW = 0
N = 1
NE = 2
E = 3
SE = 4
S = 5
SW = 6
W = 7


def parse_input():
    grove = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            grove.append(list(line.strip()))

    return grove


def enlarge_grove(grove):
    new_grove = [['.']*3*len(grove[0]) for _ in range(len(grove))]
    for row in grove:
        new_grove.append(['.'] * len(row) + row + ['.'] * len(row))
    for row in grove:
        new_grove.append(['.'] * 3 * len(row))
    return new_grove


def get_elves_coords(grove):
    coords = []
    for y in range(len(grove)):
        for x in range(len(grove[0])):
            if grove[y][x] == '#':
                coords.append((x, y))
    return coords


def get_adjacent_coords(coords):
    x = coords[X]
    y = coords[Y]

    # NW, N, NE, E, SE, S, SE, W
    return [(x-1, y-1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]


def has_elves_in_coords(grove, coords):
    for coord in coords:
        x = coord[X]
        y = coord[Y]
        if grove[y][x] == '#':
            return True

    return False


def get_north_coords(adjacent):
    return [adjacent[NW], adjacent[N], adjacent[NE]]


def get_south_coords(adjacent):
    return [adjacent[SW], adjacent[S], adjacent[SE]]


def get_west_coords(adjacent):
    return [adjacent[NW], adjacent[W], adjacent[SW]]


def get_east_coords(adjacent):
    return [adjacent[NE], adjacent[E], adjacent[SE]]


def init_grove(grove):
    new_grove = []
    for _ in range(len(grove)):
        row = []
        for _ in range(len(grove[0])):
            row.append('.')
        new_grove.append(row)
    return new_grove


def get_number_of_ground_tiles(grove):
    max_x = 0
    max_y = 0
    min_x = math.inf
    min_y = math.inf

    coords = get_elves_coords(grove)
    for coord in coords:
        x = coord[X]
        y = coord[Y]
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if x < min_x:
            min_x = x
        if y < min_y:
            min_y = y

    return (max_x - min_x + 1) * (max_y - min_y + 1) - len(coords)


def part_1(grove):
    directions = ['N', 'S', 'W', 'E']

    for _ in range(10):
        coords = get_elves_coords(grove)
        new_coords = []
        proposed = {}
        for coord in coords:
            adjacent = get_adjacent_coords(coord)
            has_elves = has_elves_in_coords(grove, adjacent)
            if has_elves:
                found_new_pos = False
                for dir in directions:
                    if dir == 'N':
                        to_check = get_north_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[N])
                            found_new_pos = True
                            break
                    elif dir == 'S':
                        to_check = get_south_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[S])
                            found_new_pos = True
                            break
                    elif dir == 'W':
                        to_check = get_west_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[W])
                            found_new_pos = True
                            break
                    elif dir == 'E':
                        to_check = get_east_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[E])
                            found_new_pos = True
                            break
                if not found_new_pos:
                    new_coords.append(coord)
            else:
                new_coords.append(coord)

        for coord in new_coords:
            if coord not in proposed:
                proposed[coord] = 1
            else:
                proposed[coord] += 1

        new_grove = init_grove(grove)
        for i in range(len(coords)):
            old_coord = coords[i]
            new_coord = new_coords[i]

            if proposed[new_coord] == 1:
                new_grove[new_coord[Y]][new_coord[X]] = '#'
            else:
                new_grove[old_coord[Y]][old_coord[X]] = '#'

        grove = new_grove
        directions = directions[1:] + [directions[0]]

    return get_number_of_ground_tiles(grove)


def part_2(grove):
    directions = ['N', 'S', 'W', 'E']
    count = 0
    moved = True

    while moved:
        count += 1
        coords = get_elves_coords(grove)
        new_coords = []
        proposed = {}
        for coord in coords:
            adjacent = get_adjacent_coords(coord)
            has_elves = has_elves_in_coords(grove, adjacent)
            if has_elves:
                found_new_pos = False
                for dir in directions:
                    if dir == 'N':
                        to_check = get_north_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[N])
                            found_new_pos = True
                            break
                    elif dir == 'S':
                        to_check = get_south_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[S])
                            found_new_pos = True
                            break
                    elif dir == 'W':
                        to_check = get_west_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[W])
                            found_new_pos = True
                            break
                    elif dir == 'E':
                        to_check = get_east_coords(adjacent)
                        if not has_elves_in_coords(grove, to_check):
                            new_coords.append(adjacent[E])
                            found_new_pos = True
                            break
                if not found_new_pos:
                    new_coords.append(coord)
            else:
                new_coords.append(coord)

        for coord in new_coords:
            if coord not in proposed:
                proposed[coord] = 1
            else:
                proposed[coord] += 1

        new_grove = init_grove(grove)
        for i in range(len(coords)):
            old_coord = coords[i]
            new_coord = new_coords[i]

            if proposed[new_coord] == 1:
                new_grove[new_coord[Y]][new_coord[X]] = '#'
            else:
                new_grove[old_coord[Y]][old_coord[X]] = '#'

        moved = grove != new_grove
        grove = new_grove
        directions = directions[1:] + [directions[0]]

    return count


if __name__ == "__main__":
    grove = parse_input()
    grove = enlarge_grove(grove)

    result_1 = part_1(grove)
    print("Part 1: ", result_1)
    result_2 = part_2(grove)
    print("Part 2: ", result_2)

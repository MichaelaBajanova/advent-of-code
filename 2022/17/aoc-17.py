import math

X = 0
Y = 1


def parse_input():
    with (open("./input.txt")) as input_file:
        return input_file.readline().strip()

# 0 - ####
#
# 1 - .#.
#     ###
#     .#.
#
# 2 - ..#
#     ..#
#     ###
#
# 3 - #
#     #
#     #
#     #
#
# 4 - ##
#     ##


def get_rock(type, bottom):
    if type == 0:
        return [(3, bottom), (4, bottom), (5, bottom), (6, bottom)]
    elif type == 1:
        return [(4, bottom+2), (3, bottom+1), (4, bottom+1), (5, bottom+1), (4, bottom)]
    elif type == 2:
        return [(5, bottom+2), (5, bottom+1), (3, bottom), (4, bottom), (5, bottom)]
    elif type == 3:
        return [(3, bottom+3), (3, bottom+2), (3, bottom+1), (3, bottom)]
    elif type == 4:
        return [(3, bottom+1), (4, bottom+1), (3, bottom), (4, bottom)]


def has_rock_stopped(placed_rock_coords, rock):
    min_y = math.inf
    for coords in rock:
        if coords[Y] < min_y:
            min_y = coords[Y]

    for coords in rock:
        if coords in placed_rock_coords:
            return True

    return min_y < 1


def move_rock_to_direction(rock, direction, placed_rock_coords):
    new_rock = []
    if direction == '>':
        max_x = 0
        for coords in rock:
            if coords[X] > max_x:
                max_x = coords[X]

        if max_x >= 7:
            return rock

        for coords in rock:
            new_rock.append((coords[X]+1, coords[Y]))

        for coords in new_rock:
            if coords in placed_rock_coords:
                return rock

    elif direction == '<':
        min_x = math.inf
        for coords in rock:
            if coords[X] < min_x:
                min_x = coords[X]

        if min_x <= 1:
            return rock

        for coords in rock:
            new_rock.append((coords[X]-1, coords[Y]))

        for coords in new_rock:
            if coords in placed_rock_coords:
                return rock

    return new_rock


def lower_rock(rock):
    new_rock = []
    for coords in rock:
        new_rock.append((coords[X], coords[Y]-1))

    return new_rock


def simulate_rocks(jet_pattern, num_of_rocks):
    placed_rock_coords = []
    height = 0
    dir_index = 0
    for i in range(num_of_rocks):
        rock_type = i % 5
        bottom_edge = height + 4
        rock = get_rock(type=rock_type, bottom=bottom_edge)

        moving_rock = rock
        while not has_rock_stopped(placed_rock_coords, rock):
            direction = jet_pattern[dir_index]
            dir_index = dir_index + 1 if dir_index < len(jet_pattern)-1 else 0
            moving_rock = move_rock_to_direction(
                rock, direction, placed_rock_coords)
            falling_rock = lower_rock(moving_rock)
            if has_rock_stopped(placed_rock_coords, rock=falling_rock):
                rock = moving_rock
                break
            rock = falling_rock

        placed_rock_coords += rock
        max_y = 0
        for coords in placed_rock_coords:
            if coords[Y] > max_y:
                max_y = coords[Y]
        height = max_y

    return height


def part_1(jet_pattern):
    return simulate_rocks(jet_pattern, num_of_rocks=2022)


def part_2(jet_pattern):
    return simulate_rocks(jet_pattern, num_of_rocks=1000000000000)


if __name__ == "__main__":
    jet_pattern = parse_input()

    result_1 = part_1(jet_pattern)
    print("Part 1: ", result_1)
    # result_2 = part_2(jet_pattern)
    # print("Part 2: ", result_2)

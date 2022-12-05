def parse_input():
    octopuses = []
    with (open("./input2.txt")) as input_file:
        for line in input_file:
            octopuses.append([int(number_as_string)
                              for number_as_string in list(line.strip())])

    return octopuses


def make_border(octopuses):
    border_row = []
    for i in range(12):
        border_row.append(0)
    octopuses.insert(0, border_row)
    octopuses.append(border_row)
    for i in range(1, 11):
        octopuses[i].insert(0, 0)
        octopuses[i].append(0)

    return octopuses


def print_octopuses(octopuses, simple=False):
    if simple:
        for y in range(1, 11):
            for x in range(1, 11):
                print(octopuses[y][x], end="")
            print()
        return

    for y in range(1, 11):
        for x in range(1, 11):
            if octopuses[y][x] < 10:
                print(octopuses[y][x], end="  ")
            else:
                print(octopuses[y][x], end=" ")
        print()


def get_adjacent_indices(x, y):
    return [
        (x-1, y-1),  # top left
        (x, y-1),  # top
        (x+1, y-1),  # top right
        (x-1, y),  # left
        (x+1, y),  # right
        (x-1, y+1),  # bottom left
        (x, y+1),  # bottom
        (x+1, y+1)  # bottom right
    ]


def is_border(coords):
    X = 0
    Y = 1
    return coords[X] == 0 or coords[Y] == 0 or coords[X] == 11 or coords[Y] == 11


def flash(octopuses, coords):
    flashed_indices = [coords]
    to_check = [coords]
    X = 0
    Y = 1
    i = 0
    while i != len(to_check):
        x = to_check[i][X]
        y = to_check[i][Y]
        adjacent = get_adjacent_indices(x, y)
        for index in adjacent:
            xx = index[X]
            yy = index[Y]
            octopuses[yy][xx] += 1
        for index in adjacent:
            xx = index[X]
            yy = index[Y]
            if octopuses[yy][xx] == 10 and (xx, yy) not in to_check and not is_border((xx, yy)):
                flashed_indices.append((xx, yy))
                to_check.append((xx, yy))
        i += 1
    return (flashed_indices, octopuses)


def part_1(octopuses):
    flashes_count = 0
    num_steps = 100
    for i in range(num_steps):
        flashed_indices = []
        for y in range(1, 11):
            for x in range(1, 11):
                octopuses[y][x] += 1

        for y in range(1, 11):
            for x in range(1, 11):
                print((x, y))
                if octopuses[y][x] > 9 and (x, y) not in flashed_indices:
                    flashed = flash(octopuses, (x, y))
                    for flashed_index in flashed[0]:
                        flashed_indices.append(flashed_index)
                    octopuses = flashed[1]

        for y in range(1, 11):
            for x in range(1, 11):
                if octopuses[y][x] >= 10:
                    octopuses[y][x] = 0

        flashes_count += len(flashed_indices)

    return flashes_count


def part_2(octopuses):
    step = 0
    while True:
        flashed_indices = set()
        flashed_count = 0
        for y in range(1, 11):
            for x in range(1, 11):
                octopuses[y][x] += 1

        for y in range(1, 11):
            for x in range(1, 11):
                if octopuses[y][x] > 9 and (x, y) not in flashed_indices:
                    flashed = flash(octopuses, (x, y))
                    for flashed_index in flashed[0]:
                        flashed_indices.add(flashed_index)
                    octopuses = flashed[1]

        for y in range(1, 11):
            for x in range(1, 11):
                if octopuses[y][x] >= 10:
                    octopuses[y][x] = 0
                    flashed_count += 1

        if flashed_count == 100:
            return step + 101
        else:
            step += 1


if __name__ == "__main__":
    octopuses = make_border(parse_input())
    result_1 = part_1(octopuses)
    print("Result 1: ", result_1)
    result_2 = part_2(octopuses)
    print("Result 2:", result_2)

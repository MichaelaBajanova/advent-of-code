X = 0
Y = 1


class Range:
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to


def parse_input():
    with (open("./input.txt")) as input_file:
        line_split = input_file.readline().split(': ')
        ranges = line_split[1]
        x_range = ranges.split(', ')[0]
        y_range = ranges.split(', ')[1]

        x_start = int(x_range.split('=')[1].split('..')[0])
        x_end = int(x_range.split('=')[1].split('..')[1])
        y_start = int(y_range.split('=')[1].split('..')[1])
        y_end = int(y_range.split('=')[1].split('..')[0])

        return {"x": Range(frm=x_start, to=x_end), "y": Range(frm=y_start, to=y_end)}


def is_probe_in_area(target_area, probe):
    x_start = target_area["x"].frm
    x_end = target_area["x"].to
    y_start = target_area["y"].frm
    y_end = target_area["y"].to

    return probe[X] >= x_start and probe[X] <= x_end and probe[Y] <= y_start and probe[Y] >= y_end


def get_next_x(x):
    if x == 0:
        return 0
    if x > 0:
        return x - 1
    if x < 0:
        return x + 1


def get_next_y(y):
    return y - 1


def print_movement(target_area, probe_positions):
    max_y = 0
    for position in probe_positions:
        if position[Y] > max_y:
            max_y = position[Y]

    print()
    print(max_y)
    for y in range(max_y, target_area["y"].to - 10, -1):
        print(y, end=" ")
        for x in range(target_area["x"].to + 10):
            if (x, y) == (0, 0):
                print("s", end=" ")
            elif (x, y) in probe_positions:
                print("#", end=" ")
            elif is_probe_in_area(target_area, (x, y)):
                print("T", end=" ")
            else:
                print('.', end=" ")
        print()
    print()


def find_x_and_positions(target_area, initial_y):
    initial_x = 0

    while abs(initial_x) < abs(target_area["x"].to):
        x = initial_x
        y = initial_y
        probe = (0, 0)
        probe_positions = []
        while True:
            probe_positions.append(probe)
            probe = (probe[X] + x, probe[Y] + y)
            if is_probe_in_area(target_area, probe):
                return {"x": initial_x, "probe_positions": probe_positions}
            if probe[X] > target_area["x"].to or probe[Y] < target_area["y"].to:
                break
            x = get_next_x(x)
            y = get_next_y(y)

        initial_x += 1

    return None


def find_x_and_positions_2(target_area, initial_y):
    initial_x = 0
    all_possible = []

    while abs(initial_x) <= abs(target_area["x"].to):
        x = initial_x
        y = initial_y
        probe = (0, 0)
        probe_positions = []
        while True:
            probe_positions.append(probe)
            probe = (probe[X] + x, probe[Y] + y)
            if is_probe_in_area(target_area, probe):
                all_possible.append(
                    {"x": initial_x, "probe_positions": probe_positions})
            if probe[X] > target_area["x"].to or probe[Y] < target_area["y"].to:
                break
            x = get_next_x(x)
            y = get_next_y(y)

        initial_x += 1

    return all_possible


def part_1(target_area):
    initial_y = 0
    prev_result = None
    maximums = []
    while abs(initial_y) <= abs(target_area["y"].to):
        result = find_x_and_positions(target_area, initial_y)
        if result is None:
            initial_y += 1
            continue

        prev_result = result

        max_y = 0
        for position in prev_result["probe_positions"]:
            if position[Y] > max_y:
                max_y = position[Y]
        if len(maximums) == 0 or max_y >= maximums[len(maximums) - 1]:
            maximums.append(max_y)
        else:
            return max_y

        initial_y += 1

    return max(maximums)


def part_2(target_area):
    initial_y = -abs(target_area["y"].to)
    initial_velocities = set()
    while initial_y <= abs(target_area["y"].to):
        all_possible = find_x_and_positions_2(target_area, initial_y)
        if len(all_possible) == 0:
            initial_y += 1
            continue

        for possible in all_possible:
            initial_velocities.add((possible["x"], initial_y))

        initial_y += 1

    return len(initial_velocities)


if __name__ == "__main__":
    target_area = parse_input()

    result_1 = part_1(target_area)
    print("Part 1: ", result_1)

    result_2 = part_2(target_area)
    print("Part 2: ", result_2)

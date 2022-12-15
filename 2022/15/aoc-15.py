X = 0
Y = 1
MAX = 4000000


class Sensor:
    def __init__(self, coords, beacon):
        self.coords = coords
        self.beacon = beacon


def parse_input():
    sensors = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.strip().split()
            sensor_x = int(line_split[2].split('=')[1][:-1])
            sensor_y = int(line_split[3].split('=')[1][:-1])
            beacon_x = int(line_split[8].split('=')[1][:-1])
            beacon_y = int(line_split[9].split('=')[1])
            sensors.append(Sensor(coords=(sensor_x, sensor_y),
                           beacon=(beacon_x, beacon_y)))

    return sensors


def get_distance(sensor, beacon):
    return abs(sensor[X] - beacon[X]) + abs(sensor[Y] - beacon[Y])


def get_beacons_on_row(sensors, row):
    beacons = []
    for sensor in sensors:
        if sensor.beacon[Y] == row:
            beacons.append(sensor.beacon)
    return beacons


def part_1(sensors):
    ROW = 2000000
    beacons_on_row = get_beacons_on_row(sensors, ROW)
    cannot_contain = set()
    for sensor in sensors:
        distance = get_distance(sensor.coords, sensor.beacon)
        row_distance = abs(sensor.coords[Y] - ROW)
        if row_distance <= distance:
            for x in range(distance-row_distance+1):  # go to the sides
                right = (sensor.coords[X]+x, ROW)
                left = (sensor.coords[X]-x, ROW)
                if right not in beacons_on_row:
                    cannot_contain.add(right)
                if left not in beacons_on_row:
                    cannot_contain.add(left)

    return len(cannot_contain)


def calculate_tuning_frequency(beacon):
    return beacon[X]*4000000 + beacon[Y]


def get_sensor_range(sensor):
    distance = get_distance(sensor.coords, sensor.beacon)
    x = sensor.coords[X]
    y = sensor.coords[Y]
    # up, right, down, left (points)
    return ((x, y-distance), (x+distance, y), (x, y+distance), (x-distance, y))


def is_valid_border_point(point):
    x = point[X]
    y = point[Y]
    return x >= 0 and x <= MAX and y >= 0 and y <= MAX


def get_sensor_border(sensor_range):
    border = set()

    # up -> right
    up = sensor_range[0]
    up = (up[X], up[Y]-1)
    right = sensor_range[1]
    right = (right[X]+1, right[Y])

    for i in range(abs(up[X] - right[X])):
        new_point = (up[X] + i, up[Y] + i)
        if is_valid_border_point(new_point):
            border.add(new_point)

    # right -> down
    for i in range(abs(up[X] - right[X])):
        new_point = (right[X] - i, right[Y] + i)
        if is_valid_border_point(new_point):
            border.add(new_point)

    # down -> left
    down = sensor_range[2]
    down = (down[X], down[Y]+1)
    for i in range(abs(up[X] - right[X])):
        new_point = (down[X] - i, down[Y] - i)
        if is_valid_border_point(new_point):
            border.add(new_point)

    # left -> up
    left = sensor_range[3]
    left = (left[X]-1, left[Y])
    for i in range(abs(up[X] - left[X])):
        new_point = (up[X] - i, up[Y] + i)
        if is_valid_border_point(new_point):
            border.add(new_point)

    return border


def is_point_on_left(point, line):
    point_A = line[0]
    point_B = line[1]

    # D = (x2 - x1) * (yp - y1) - (xp - x1) * (y2 - y1)
    return (point_B[X] - point_A[X]) * (point[Y] - point_A[Y]) - (point[X] - point_A[X]) * (point_B[Y] - point_A[Y]) >= 0


def is_in_range(range, point):
    if not is_point_on_left(point, [range[0], range[1]]):
        return False
    if not is_point_on_left(point, [range[1], range[2]]):
        return False
    if not is_point_on_left(point, [range[2], range[3]]):
        return False
    if not is_point_on_left(point, [range[3], range[0]]):
        return False

    return True


# takes several minutes, but it's good enough for me
def part_2(sensors):
    border_points = set()
    for sensor in sensors:
        sensor_range = get_sensor_range(sensor)
        sensor_border = get_sensor_border(sensor_range)
        border_points.update(sensor_border)

    for point in border_points:
        is_in_sensor_range = False
        for sensor in sensors:
            sensor_range = get_sensor_range(sensor)
            if is_in_range(range=sensor_range, point=point):
                is_in_sensor_range = True
        if not is_in_sensor_range:
            return calculate_tuning_frequency(point)

    return 0


if __name__ == "__main__":
    sensors = parse_input()

    result_1 = part_1(sensors)
    print("Part 1: ", result_1)
    result_2 = part_2(sensors)
    print("Part 2: ", result_2)

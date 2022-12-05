def get_heightmap():
    heightmap = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            heightmap.append([int(number_as_string)
                              for number_as_string in list(line.strip())])

    return heightmap


def is_lowpoint(location_heights, this_height):
    for height in location_heights:
        if height <= this_height:
            return False
    return True


def part_1(heightmap):
    risk = 0
    max_y = len(heightmap) - 1
    max_x = len(heightmap[0]) - 1
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            this_height = heightmap[y][x]
            location_heights = []
            # up
            if y > 0:
                location_heights.append(heightmap[y - 1][x])
            # right
            if x < max_x:
                location_heights.append(heightmap[y][x + 1])
            # down
            if y < max_y:
                location_heights.append(heightmap[y + 1][x])
            # left
            if x > 0:
                location_heights.append(heightmap[y][x - 1])

            if is_lowpoint(location_heights, this_height):
                risk += this_height + 1

    return risk


def print_heightmap(heightmap):
    for row in heightmap:
        for h in row:
            print(h, end="")
        print()


class Height:
    def __init__(self, height, is_basin):
        self.height = height
        self.is_basin = is_basin


def search(heightmap, coords):
    basin_size = 1
    to_check = [coords]
    X = 0
    Y = 1
    i = 0
    while i != len(to_check):
        x = to_check[i][X]
        y = to_check[i][Y]
        if heightmap[y-1][x] != 9 and (x, y-1) not in to_check:  # up
            to_check.append((x, y-1))
            basin_size += 1
        if heightmap[y][x+1] != 9 and (x+1, y) not in to_check:  # right
            to_check.append((x+1, y))
            basin_size += 1
        if heightmap[y+1][x] != 9 and (x, y+1) not in to_check:  # down
            to_check.append((x, y+1))
            basin_size += 1
        if heightmap[y][x-1] != 9 and (x-1, y) not in to_check:  # left
            to_check.append((x-1, y))
            basin_size += 1
        i += 1
    return basin_size


def part_2(heightmap):
    result = 1  # not 0 because we will multiply
    width = len(heightmap[0])
    border_row = []
    for i in range(width + 2):
        border_row.append(9)
    # add border row at the top and bottom
    heightmap.insert(0, border_row)
    heightmap.append(border_row)
    # add border left and right
    for i in range(len(heightmap)):
        if i == 0 or i == len(heightmap) - 1:
            continue
        heightmap[i].insert(0, 9)
        heightmap[i].append(9)

    basin_sizes = []
    for y in range(1, len(heightmap) - 1):
        for x in range(1, len(heightmap[y]) - 1):
            this_height = heightmap[y][x]
            location_heights = []
            location_heights.append(heightmap[y - 1][x])  # up
            location_heights.append(heightmap[y][x + 1])  # right
            location_heights.append(heightmap[y + 1][x])  # down
            location_heights.append(heightmap[y][x - 1])  # left
            if is_lowpoint(location_heights, this_height):
                basin_size = search(heightmap, (x, y))
                basin_sizes.append(basin_size)

    sorted_sizes = sorted(basin_sizes, reverse=True)
    for i in range(3):
        result *= sorted_sizes[i]
    return result


if __name__ == "__main__":
    heightmap = get_heightmap()
    risk_of_lowpoints = part_1(heightmap)
    print("Part 1: ", risk_of_lowpoints)
    result = part_2(heightmap)
    print("Part 2: ", result)

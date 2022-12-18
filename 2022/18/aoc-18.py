X = 0
Y = 1
Z = 2


def parse_input():
    coords = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.strip().split(',')
            x = int(line_split[X])
            y = int(line_split[Y])
            z = int(line_split[Z])
            coords.append((x, y, z))

    return coords


def are_cubes_touching_x(cube_1, cube_2):
    touching_x = abs(cube_1[X] - cube_2[X]) == 1
    same_y = cube_1[Y] == cube_2[Y]
    same_z = cube_1[Z] == cube_2[Z]
    return touching_x and same_y and same_z


def are_cubes_touching_y(cube_1, cube_2):
    touching_y = abs(cube_1[Y] - cube_2[Y]) == 1
    same_x = cube_1[X] == cube_2[X]
    same_z = cube_1[Z] == cube_2[Z]
    return same_x and touching_y and same_z


def are_cubes_touching_z(cube_1, cube_2):
    touching_z = abs(cube_1[Z] - cube_2[Z]) == 1
    same_x = cube_1[X] == cube_2[X]
    same_y = cube_1[Y] == cube_2[Y]
    return same_x and same_y and touching_z


def are_cubes_touching(cube_1, cube_2):
    if are_cubes_touching_x(cube_1, cube_2):
        return True

    if are_cubes_touching_y(cube_1, cube_2):
        return True

    if are_cubes_touching_z(cube_1, cube_2):
        return True

    return False


def get_max_xyz(cubes):
    max_x = 0
    max_y = 0
    max_z = 0
    for cube in cubes:
        if cube[X] > max_x:
            max_x = cube[X]
        if cube[Y] > max_y:
            max_y = cube[Y]
        if cube[Z] > max_z:
            max_z = cube[Z]

    return (max_x, max_y, max_z)


def spread(cubes, from_cube):
    max_xyz = get_max_xyz(cubes)
    max_x = max_xyz[X]
    max_y = max_xyz[Y]
    max_z = max_xyz[Z]

    visited = []
    queue = [from_cube]
    while len(queue) > 0:
        to_spread = queue.pop()
        visited.append(to_spread)
        left = (to_spread[X]-1, to_spread[Y], to_spread[Z])
        right = (to_spread[X]+1, to_spread[Y], to_spread[Z])
        bottom = (to_spread[X], to_spread[Y]-1, to_spread[Z])
        top = (to_spread[X], to_spread[Y]+1, to_spread[Z])
        front = (to_spread[X], to_spread[Y], to_spread[Z]-1)
        back = (to_spread[X], to_spread[Y], to_spread[Z]+1)

        if left[X] >= -1 and left not in cubes and left not in visited:
            queue.append(left)
        if right[X] <= max_x + 1 and right not in cubes and right not in visited:
            queue.append(right)

        if bottom[Y] >= -1 and bottom not in cubes and bottom not in visited:
            queue.append(bottom)
        if top[Y] <= max_y + 1 and top not in cubes and top not in visited:
            queue.append(top)

        if front[Z] >= -1 and front not in cubes and front not in visited:
            queue.append(front)
        if back[Z] <= max_z + 1 and back not in cubes and back not in visited:
            queue.append(back)

    return visited


def get_inner_empty_cubes(cubes):
    cubes_without_air_bubbles = cubes

    max_xyz = get_max_xyz(cubes)
    max_x = max_xyz[X]
    max_y = max_xyz[Y]
    max_z = max_xyz[Z]

    spread_cubes = spread(cubes, (-1, -1, -1))
    cubes_without_air_bubbles += spread_cubes

    empty_cubes = []
    for x in range(max_x+1):
        for y in range(max_y+1):
            for z in range(max_z+1):
                if (x, y, z) not in cubes_without_air_bubbles:
                    empty_cubes.append((x, y, z))

    return empty_cubes


def part_1(coords):
    result = 0
    for i in range(len(coords)):
        exposed = 6
        for j in range(len(coords)):
            if i == j:
                continue
            if are_cubes_touching(coords[i], coords[j]):
                exposed -= 1
        result += exposed

    return result


def part_2(coords, all_exposed):
    inner_empty_cubes = get_inner_empty_cubes(coords)
    result = all_exposed
    for cube in coords:
        for empty_cube in inner_empty_cubes:
            if are_cubes_touching(cube, empty_cube):
                result -= 1

    return result


if __name__ == "__main__":
    coords = parse_input()
    result_1 = part_1(coords)
    print("Part 1: ", result_1)
    result_2 = part_2(coords, result_1)
    print("Part 2: ", result_2)

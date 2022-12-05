def get_directions():
    directions = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            directions.append(line)

    return directions


def simple(directions):
    depth = 0
    horizontal = 0
    for direction in directions:
        direction_split = direction.split()
        if direction_split[0] == "forward":
            horizontal += int(direction_split[1])
        if direction_split[0] == "up":
            depth -= int(direction_split[1])
        if direction_split[0] == "down":
            depth += int(direction_split[1])

    print("Depth: ", depth)
    print("Horizontal: ", horizontal)
    print("Depth x Horizontal = ", depth * horizontal)


def advanced(directions):
    depth = 0
    horizontal = 0
    aim = 0

    for direction in directions:
        direction_split = direction.split()
        if direction_split[0] == "forward":
            horizontal += int(direction_split[1])
            depth += aim * int(direction_split[1])
        if direction_split[0] == "up":
            aim -= int(direction_split[1])
        if direction_split[0] == "down":
            aim += int(direction_split[1])

    print("Depth: ", depth)
    print("Horizontal: ", horizontal)
    print("Depth x Horizontal = ", depth * horizontal)


if __name__ == "__main__":
    directions = get_directions()
    simple(directions)
    advanced(directions)

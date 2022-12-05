def get_depths():
    depths = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            depths.append(int(line))

    return depths


def simple(depths):
    increase_count = 0
    for i in range(len(depths) - 1):
        if depths[i] < depths[i + 1]:
            increase_count += 1

    print(increase_count)


def advanced(depths):
    window_depths = []
    for i in range(len(depths) - 2):
        window_depth = depths[i] + depths[i + 1] + depths[i + 2]
        window_depths.append(window_depth)

    simple(window_depths)


if __name__ == "__main__":
    depths = get_depths()
    simple(depths)
    advanced(depths)

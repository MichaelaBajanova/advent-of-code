def get_trees():
    trees = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            trees.append([int(number_as_string)
                          for number_as_string in list(line.strip())])

    return trees


def is_tree_visible(coords, tree, width, height):
    x = coords[0]
    y = coords[1]
    not_visible_count = 0
    # up
    for yy in range(0, y):
        if trees[yy][x] >= tree:
            not_visible_count += 1
            break
    # right
    for xx in range(x+1, width):
        if trees[y][xx] >= tree:
            not_visible_count += 1
            break
    # down
    for yy in range(y+1, height):
        if trees[yy][x] >= tree:
            not_visible_count += 1
            break
    # left
    for xx in range(0, x):
        if trees[y][xx] >= tree:
            not_visible_count += 1
            break

    return not_visible_count < 4


def part_1(trees):
    result = 0
    height = len(trees)
    width = len(trees[0])
    result += 2*height + 2*width - 4
    for y in range(1, height-1):
        for x in range(1, width-1):
            tree = trees[y][x]
            if tree == 0:
                continue
            if is_tree_visible((x, y), tree, width, height):
                result += 1

    return result


def part_2(trees):
    scores = []
    height = len(trees)
    width = len(trees[0])
    for y in range(1, height-1):
        for x in range(1, width-1):
            tree = trees[y][x]
            up = 0
            right = 0
            down = 0
            left = 0
            # up
            for yy in range(y-1, -1, -1):
                up += 1
                if trees[yy][x] >= tree:
                    break
            # right
            for xx in range(x+1, width):
                right += 1
                if trees[y][xx] >= tree:
                    break
            # down
            for yy in range(y+1, height):
                down += 1
                if trees[yy][x] >= tree:
                    break

            # left
            for xx in range(x-1, -1, -1):
                left += 1
                if trees[y][xx] >= tree:
                    break

            scores.append(up * right * down * left)

    return max(scores)


if __name__ == "__main__":
    trees = get_trees()
    result_1 = part_1(trees)
    print("Part 1: ", result_1)
    result_2 = part_2(trees)
    print("Part 2: ", result_2)

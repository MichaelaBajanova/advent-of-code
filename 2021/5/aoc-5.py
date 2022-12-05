def get_board_size():
    max_x = 0
    max_y = 0
    with (open("./input.txt")) as input_file:
        for file_line in input_file:
            line = file_line.split(" -> ")
            start_coords = line[0].split(",")
            end_coords = line[1].split(",")
            x1 = int(start_coords[0])
            y1 = int(start_coords[1])
            x2 = int(end_coords[0])
            y2 = int(end_coords[1])
            if x1 > max_x:
                max_x = x1
            if x2 > max_x:
                max_x = x2
            if y1 > max_y:
                max_y = y1
            if y2 > max_y:
                max_y = y2

    return (max_x, max_y)


def print_vents(vents):
    for row in vents:
        for column in row:
            if column == 0:
                print(".", end=" ")
            else:
                print(column, end=" ")
        print()


def simple(board_size):
    vents = []
    for _ in range(board_size[1] + 1):
        vents.append([0] * (board_size[0] + 1))

    with (open("./input.txt")) as input_file:
        for file_line in input_file:
            line = file_line.split(" -> ")
            start_coords = line[0].split(",")
            end_coords = line[1].split(",")
            x1 = int(start_coords[0])
            y1 = int(start_coords[1])
            x2 = int(end_coords[0])
            y2 = int(end_coords[1])

            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        vents[y][x1] += 1
                if y2 < y1:
                    for y in range(y2, y1 + 1):
                        vents[y][x1] += 1
            if y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        vents[y1][x] += 1
                if x2 < x1:
                    for x in range(x2, x1 + 1):
                        vents[y1][x] += 1

    count = 0
    for row in vents:
        for vent in row:
            if vent >= 2:
                count += 1

    print(count)


def advanced(board_size):
    vents = []
    for _ in range(board_size[1] + 1):
        vents.append([0] * (board_size[0] + 1))

    with (open("./input.txt")) as input_file:
        for file_line in input_file:
            line = file_line.split(" -> ")
            start_coords = line[0].split(",")
            end_coords = line[1].split(",")
            x1 = int(start_coords[0])
            y1 = int(start_coords[1])
            x2 = int(end_coords[0])
            y2 = int(end_coords[1])

            # vertical
            if x1 == x2:
                if y1 < y2:
                    for y in range(y1, y2 + 1):
                        vents[y][x1] += 1
                if y2 < y1:
                    for y in range(y2, y1 + 1):
                        vents[y][x1] += 1

            # horizontal
            elif y1 == y2:
                if x1 < x2:
                    for x in range(x1, x2 + 1):
                        vents[y1][x] += 1
                if x2 < x1:
                    for x in range(x2, x1 + 1):
                        vents[y1][x] += 1

            # diagonal
            else:
                if x1 < x2 and y1 < y2:
                    span = x2 - x1 + 1
                    for i in range(span):
                        vents[y1 + i][x1 + i] += 1

                if x1 < x2 and y1 > y2:
                    span = x2 - x1 + 1
                    for i in range(span):
                        vents[y1 - i][x1 + i] += 1

                if x1 > x2 and y1 < y2:
                    span = x1 - x2 + 1
                    for i in range(span):
                        vents[y1 + i][x1 - i] += 1

                if x1 > x2 and y1 > y2:
                    span = x1 - x2 + 1
                    for i in range(span):
                        vents[y1 - i][x1 - i] += 1

    count = 0
    for row in vents:
        for vent in row:
            if vent >= 2:
                count += 1

    print(count)


if __name__ == "__main__":
    board_size = get_board_size()
    simple(board_size)
    advanced(board_size)

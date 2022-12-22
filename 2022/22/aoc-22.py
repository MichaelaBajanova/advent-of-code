X = 0
Y = 1


def fill_board(board):
    max_row_len = 0
    for row in board:
        row_len = len(row)
        if row_len > max_row_len:
            max_row_len = row_len

    new_board = []
    for row in board:
        new_row = []
        for tile in row:
            new_row.append(tile)

        if len(new_row) < max_row_len:
            for _ in range(max_row_len - len(new_row)):
                new_row.append(None)

        new_board.append(new_row)

    return new_board


def parse_input():
    reading_directions = False
    board = []
    numbers = None
    turns = None
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            if len(line_strip) == 0:
                reading_directions = True
                continue

            if reading_directions:
                numbers_str = line_strip.replace(
                    'R', ' ').replace('L', ' ').split()
                numbers = [int(number) for number in numbers_str]
                turns = list(line_strip.replace(
                    '0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', ''))
                continue

            board_line = line.replace('\n', '')
            row = []
            for char in board_line:
                if char == ' ':
                    row.append(None)
                else:
                    row.append(char)

            board.append(row)

    board = fill_board(board)

    return {"board": board, "numbers": numbers, "turns": turns}


def print_board(board):
    for row in board:
        for tile in row:
            if tile is None:
                print(" ", end="")
            else:
                print(tile, end="")
        print()


def get_starting_pos_in_row(board, row):
    x = 0
    for i in range(len(board[row])):
        if board[row][i] is not None:
            x = i
            break

    return (x, row)


def get_last_pos_in_row(board, row):
    x = len(board[row]) - 1
    for i in range(len(board[row])-1, -1, -1):
        if board[row][i] is not None:
            x = i
            break

    return (x, row)


def get_starting_pos_in_col(board, col):
    y = 0
    for i in range(len(board)):
        if board[i][col] is not None:
            y = i
            break

    return (col, y)


def get_last_pos_in_col(board, col):
    y = len(board) - 1
    for i in range(len(board)-1, -1, -1):
        if board[i][col] is not None:
            y = i
            break

    return (col, y)


def make_turn(facing, turn):
    deg = 0
    if facing == "right":
        deg = 90
    elif facing == "down":
        deg = 180
    elif facing == "left":
        deg = 270

    deg = (deg + 90) % 360 if turn == "R" else (deg - 90 + 360) % 360

    if deg == 0:
        return "up"
    elif deg == 90:
        return "right"
    elif deg == 180:
        return "down"
    elif deg == 270:
        return "left"


def off_board(state, board):
    pos = state["pos"]
    facing = state["facing"]
    x = pos[X]
    y = pos[Y]

    if x < 0:
        return get_last_pos_in_row(board, row=y)
    if y < 0:
        return get_last_pos_in_col(board, col=x)
    if x >= len(board[0]):
        return get_starting_pos_in_row(board, row=y)
    if y >= len(board):
        return get_starting_pos_in_col(board, col=x)
    if board[y][x] is None:
        if facing == "up":
            return get_last_pos_in_col(board, col=x)
        elif facing == "right":
            return get_starting_pos_in_row(board, row=y)
        elif facing == "down":
            return get_starting_pos_in_col(board, col=x)
        elif facing == "left":
            return get_last_pos_in_row(board, row=y)

    return pos


def go_forward_and_turn(board, state, forward, turn):
    pos = state["pos"]
    facing = state["facing"]

    moved = 0
    new_pos = pos
    while board[pos[Y]][pos[X]] != '#' and moved <= forward:
        new_pos = pos
        x = pos[X]
        y = pos[Y]
        if facing == "up":
            pos = (x, y-1)
        elif facing == "right":
            pos = (x+1, y)
        elif facing == "down":
            pos = (x, y+1)
        elif facing == "left":
            pos = (x-1, y)

        pos = off_board(state={"pos": pos, "facing": facing}, board=board)
        moved += 1

    if turn is not None:
        facing = make_turn(facing, turn)

    return {"pos": new_pos, "facing": facing}


def calculate_password(state):
    pos = state["pos"]
    facing = state["facing"]
    facing_value = 0  # right
    if facing == "up":
        facing_value = 3
    elif facing == "down":
        facing_value == 1
    elif facing == "left":
        facing_value = 2

    return ((pos[Y]+1) * 1000) + ((pos[X]+1) * 4) + facing_value


def off_cube_side(state, board):
    pos = state["pos"]
    facing = state["facing"]
    x = pos[X]
    y = pos[Y]

    if y == -1 and x >= 50 and x < 100 and facing == "up":
        new_x = 0
        new_y = x + 100
        new_facing = "right"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if y == -1 and x >= 100 and x < len(board[0]) and facing == "up":
        new_x = x - 100
        new_y = 199
        new_facing = "up"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == len(board[0]) and y >= 0 and y < 50 and facing == "right":
        new_x = 99
        new_y = 149 - y
        new_facing = "left"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if y == 50 and x >= 100 and x < len(board[0]) and facing == "down":
        new_x = 99
        new_y = x - 50
        new_facing = "left"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == 100 and y >= 50 and y < 100 and facing == "right":
        new_x = y + 50
        new_y = 49
        new_facing = "up"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == 100 and y >= 100 and y < 150 and facing == "right":
        new_x = 149
        new_y = 149 - y
        new_facing = "left"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if y == 150 and x >= 50 and x < 100 and facing == "down":
        new_x = 49
        new_y = x + 100
        new_facing = "left"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == 50 and y >= 150 and y < len(board) and facing == "right":
        new_x = y - 100
        new_y = 149
        new_facing = "up"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if y == len(board) and x >= 0 and x < 50 and facing == "down":
        new_x = x + 100
        new_y = 0
        new_facing = "down"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == -1 and y >= 150 and y < len(board) and facing == "left":
        new_x = y - 100
        new_y = 0
        new_facing = "down"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == -1 and y >= 100 and y < 150 and facing == "left":
        new_x = 50
        new_y = 149 - y
        new_facing = "right"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if y == 99 and x >= 0 and x < 50 and facing == "up":
        new_x = 50
        new_y = x + 50
        new_facing = "right"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == 49 and y >= 50 and y < 100 and facing == "left":
        new_x = y - 50
        new_y = 100
        new_facing = "down"
        return {"pos": (new_x, new_y), "facing": new_facing}
    if x == 49 and y >= 0 and y < 50 and facing == "left":
        new_x = 0
        new_y = 149 - y
        new_facing = "right"
        return {"pos": (new_x, new_y), "facing": new_facing}

    return {"pos": pos, "facing": facing}


def go_forward_and_turn_2(board, state, forward, turn):
    pos = state["pos"]
    facing = state["facing"]

    moved = 0
    new_pos = pos
    new_facing = facing
    while board[pos[Y]][pos[X]] != '#' and moved <= forward:
        new_pos = pos
        new_facing = facing
        x = pos[X]
        y = pos[Y]
        if facing == "up":
            pos = (x, y-1)
        elif facing == "right":
            pos = (x+1, y)
        elif facing == "down":
            pos = (x, y+1)
        elif facing == "left":
            pos = (x-1, y)

        new_state = off_cube_side(
            state={"pos": pos, "facing": facing}, board=board)
        pos = new_state["pos"]
        facing = new_state["facing"]
        moved += 1

    if turn is not None:
        new_facing = make_turn(new_facing, turn)

    return {"pos": new_pos, "facing": new_facing}


def part_1(board, numbers, turns):
    pos = get_starting_pos_in_row(board, row=0)
    facing = "right"
    state = {"pos": pos, "facing": facing}

    for number_i in range(len(numbers)):
        number = numbers[number_i]
        turn = turns[number_i] if number_i < len(turns) else None
        state = go_forward_and_turn(board, state, number, turn)

    return calculate_password(state)


def part_2(board, numbers, turns):
    pos = get_starting_pos_in_row(board, row=0)
    facing = "right"
    state = {"pos": pos, "facing": facing}

    for number_i in range(len(numbers)):
        number = numbers[number_i]
        turn = turns[number_i] if number_i < len(turns) else None
        state = go_forward_and_turn_2(board, state, number, turn)

    return calculate_password(state)


if __name__ == "__main__":
    parsed = parse_input()
    board = parsed["board"]
    numbers = parsed["numbers"]
    turns = parsed["turns"]

    result_1 = part_1(board, numbers, turns)
    print("Part 1: ", result_1)
    result_2 = part_2(board, numbers, turns)
    print("Part 2: ", result_2)

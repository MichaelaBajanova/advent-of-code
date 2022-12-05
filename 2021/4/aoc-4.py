def get_called_numbers():
    called_numbers = []
    with (open("./input.txt")) as input_file:
        line = input_file.readline()
        called_numbers = line.split(",")

    return [int(number_as_string) for number_as_string in called_numbers]


def get_boards():
    boards = []
    lines = []
    with (open("./input.txt")) as input_file:
        lines = input_file.readlines()

    board_lines = list(filter(lambda line: line != "\n", lines[2:]))
    for i in range(len(board_lines) - 4):
        if i % 5 == 0:
            board = board_lines[i].split() + board_lines[i+1].split() + \
                board_lines[i+2].split() + board_lines[i+3].split() + \
                board_lines[i+4].split()
            boards.append([int(number_as_string)
                          for number_as_string in board])

    return boards


def is_winning_board(marked):
    for i in range(25):
        # rows
        if i % 5 == 0:
            if marked[i] == 1 and marked[i+1] == 1 and marked[i+2] == 1 and marked[i+3] == 1 and marked[i+4] == 1:
                return True
        # columns
        if i < 5:
            if marked[i] == 1 and marked[i+5] == 1 and marked[i+10] == 1 and marked[i+15] == 1 and marked[i+20] == 1:
                return True

    return False


def calculate_score(board_numbers, called_numbers):
    unmarked_numbers = list(filter(
        lambda number: number not in called_numbers, board_numbers))
    sum = 0
    for number in unmarked_numbers:
        sum += number

    return sum * called_numbers[len(called_numbers) - 1]


def first_winning_board_score(boards, called_numbers):
    marked = []
    for _ in range(len(boards)):
        marked.append([0] * 25)

    for i in range(len(called_numbers)):
        for board_index in range(len(boards)):
            for number_index in range(len(boards[board_index])):
                if called_numbers[i] == boards[board_index][number_index]:
                    marked[board_index][number_index] = 1
            if is_winning_board(marked[board_index]):
                print("First winning board score: ", calculate_score(
                    boards[board_index], called_numbers[0:i+1]))
                return


def last_winning_board_score(boards, called_numbers):
    won = []
    marked = []
    for _ in range(len(boards)):
        won.append(False)
        marked.append([0] * 25)

    for i in range(len(called_numbers)):
        for board_index in range(len(boards)):
            for number_index in range(len(boards[board_index])):
                if called_numbers[i] == boards[board_index][number_index]:
                    marked[board_index][number_index] = 1
            if is_winning_board(marked[board_index]):
                won[board_index] = True
                if all(won):
                    print("Last winning board score: ", calculate_score(
                        boards[board_index], called_numbers[0:i+1]))
                    return


if __name__ == "__main__":
    called_numbers = get_called_numbers()
    boards = get_boards()
    first_winning_board_score(boards, called_numbers)
    last_winning_board_score(boards, called_numbers)

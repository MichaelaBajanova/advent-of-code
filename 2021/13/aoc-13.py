class Instruction:
    def __init__(self, direction, index):
        self.direction = direction
        self.index = index


def print_dots(dots):
    for row in dots:
        for ch in row:
            print(ch, end="")
        print()


def get_dots_and_instructions():
    is_reading_instructions = False
    dot_indices = []
    instructions = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            if len(line_strip) == 0:
                is_reading_instructions = True
                continue
            if not is_reading_instructions:
                line_split = line_strip.split(',')
                x = int(line_split[0])
                y = int(line_split[1])
                dot_indices.append((x, y))
            else:
                line_split = line_strip.split()
                instruction_split = line_split[2].split('=')
                direction = "vertical" if instruction_split[0] == "x" else "horizontal"
                index = int(instruction_split[1])
                instructions.append(Instruction(direction, index))

    dots = []
    # find max x and max y
    max_x = 0
    max_y = 0
    for indices in dot_indices:
        x = indices[0]
        y = indices[1]
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    for y in range(max_y + 1):
        row = []
        for x in range(max_x + 1):
            row.append('.')
        dots.append(row)

    for indices in dot_indices:
        x = indices[0]
        y = indices[1]
        dots[y][x] = '#'

    return {"dots": dots, "instructions": instructions}


def split_horizontally(dots, index):
    return [dots[:index], dots[index+1:]]


def split_vertically(dots, index):
    section_1 = []
    section_2 = []

    for row in dots:
        new_row = []
        for i in range(len(row)):
            if i < index:
                new_row.append(row[i])
        section_1.append(new_row)

    for row in dots:
        new_row = []
        for i in range(len(row)):
            if i > index:
                new_row.append(row[i])
        section_2.append(new_row)

    return [section_1, section_2]


def split_dots(dots, instruction):
    if instruction.direction == 'horizontal':
        return split_horizontally(dots, instruction.index)
    elif instruction.direction == 'vertical':
        return split_vertically(dots, instruction.index)


def transpose_matrix(matrix):
    result = []
    for _ in range(len(matrix[0])):
        result.append([])

    for row in matrix:
        for i in range(len(row)):
            result[i].append(row[i])

    return result


def mirror_along_x(dots):
    mirrored = []
    for row in dots:
        row.reverse()
        mirrored.append(row)
    return mirrored


def mirror_along_y(dots):
    transposed = transpose_matrix(dots)
    return transpose_matrix(mirror_along_x(transposed))


def mirror_dots(dots, direction):
    if direction == 'horizontal':
        return mirror_along_y(dots)
    elif direction == 'vertical':
        return mirror_along_x(dots)


def get_dots_after_instructions(dots, instructions, num_of_instructions):
    result = 0

    current_dots = [*dots]
    for i in range(num_of_instructions):
        instruction = instructions[i]
        dots_split = split_dots(current_dots, instruction)
        to_mirror = dots_split[1]
        dots_mirrored = mirror_dots(to_mirror, instruction.direction)
        new_dots = []
        for j in range(len(dots_mirrored)):
            row_1 = dots_split[0][j]
            row_2 = dots_mirrored[j]
            new_row = []
            for k in range(len(row_1)):
                if row_1[k] == '#' or row_2[k] == '#':
                    new_row.append('#')
                else:
                    new_row.append('.')
            new_dots.append(new_row)
        current_dots = [*new_dots]

    return current_dots


if __name__ == "__main__":
    parsed = get_dots_and_instructions()
    dots = parsed["dots"]
    instructions = parsed["instructions"]

    dots_1 = get_dots_after_instructions(
        dots, instructions, num_of_instructions=1)
    result_1 = 0
    for row in dots_1:
        for dot in row:
            if dot == '#':
                result_1 += 1
    print("Part 1: ", result_1)

    dots_2 = get_dots_after_instructions(
        dots, instructions, num_of_instructions=len(instructions))
    print_dots(dots_2)

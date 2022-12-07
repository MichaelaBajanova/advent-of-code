class Directory:
    def __init__(self, name, children, parent):
        self.name = name
        self.children = children
        self.parent = parent


class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def parse_input():
    lines = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            line_split = line_strip.split()

            if line_split[0] == '$':
                if line_split[1] == "cd":
                    lines.append({"cd": line_split[2]})
                elif line_split[1] == "ls":
                    lines.append({"ls": ""})
            else:
                if line_split[0] == "dir":
                    lines.append({"dir": line_split[1]})
                else:
                    lines.append({line_split[1]: line_split[0]})

    return lines


def get_size(item):
    if isinstance(item, File):
        return item.size

    size = 0
    for child in item.children:
        size += get_size(child)
    return size


def get_sizes(item):
    sizes = []
    to_check = [item]
    i = 0

    while len(to_check) > 0:
        item_to_check = to_check.pop()
        if isinstance(item_to_check, Directory):
            to_check += item_to_check.children
            sizes.append(get_size(item_to_check))
        i += 1

    return sizes


def get_root(console):
    reading_items = False
    root = Directory(name="/", children=[], parent=None)
    current_directory = root
    for command in console:
        if "ls" in command:
            reading_items = True
            continue
        if "cd" in command:
            reading_items = False
            cd_to = command["cd"]
            if cd_to == "/":
                current_directory = root
            elif cd_to == "..":
                current_directory = current_directory.parent
            else:
                current_directory = next(
                    (child for child in current_directory.children if child.name == cd_to), None)

        if reading_items:
            item = None
            if "dir" in command:
                item = Directory(name=command["dir"], children=[
                ], parent=current_directory)
            else:
                name = next(iter(command))
                item = File(name, size=int(command[name]))
            current_directory.children.append(item)

    return root


def part_1(console):
    root = get_root(console)
    sizes = get_sizes(root)
    result = 0
    for i in range(1, len(sizes)):
        if sizes[i] <= 100000:
            result += sizes[i]

    return result


def part_2(console):
    TOTAL = 70000000
    NEED = 30000000
    root = get_root(console)
    root_size = get_size(root)
    available_space = TOTAL - root_size
    to_delete_space = NEED - available_space
    sizes = get_sizes(root)
    can_delete = []
    for i in range(1, len(sizes)):
        if sizes[i] >= to_delete_space:
            can_delete.append(sizes[i])
    min = can_delete[0]
    for item in can_delete:
        if min > item:
            min = item

    return min


if __name__ == "__main__":
    console = parse_input()
    result_1 = part_1(console)
    print("Part 1: ", result_1)
    result_2 = part_2(console)
    print("Part 2: ", result_2)

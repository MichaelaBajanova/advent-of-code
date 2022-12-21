import copy

INPUT_FILE = "./input.txt"


class CircularLinkedList:
    def __init__(self, value, left, right, is_first=False):
        self.value = value
        self.left = left
        self.right = right
        self.is_first = is_first

    def print(self):
        start = self
        print(start.value, end=" ")
        start = start.right
        i = 0
        while i < 8:
            print(start.value, end=" ")
            start = start.right
            i += 1
        print()

    def get_size(self):
        current = self

        size = 0
        while current.right is not self:
            current = current.right
            size += 1

        return size+1

    def add_node(self, value):
        if self.value is None:
            self.value = value
            self.is_first = True
            self.right = self
            self.left = self
            return self

        add_to = self
        while not add_to.right.is_first:
            add_to = add_to.right

        new_node = CircularLinkedList(value, left=add_to, right=self)
        self.left = new_node
        add_to.right = new_node

    def remove_node(self):
        self.left.right = self.right
        self.right.left = self.left

        return self.left

    def insert_node(self, index, value):
        size = self.get_size()
        insert_to = index % size if index > 0 else -(abs(index) % size)
        current = self

        if insert_to > 0:
            i = 0
            while i < insert_to:
                current = current.right
                i += 1

        if insert_to < 0:
            i = 0
            while i > insert_to:
                current = current.left
                i -= 1

        left = current
        right = current.right
        new_node = CircularLinkedList(value, left, right)
        left.right = new_node
        right.left = new_node

        return new_node

    def get_grove_coords_sum(self):
        current = self
        while current.value != 0:
            current = current.right

        result = 0
        i = 0
        while i < 1000:
            current = current.right
            i += 1
        result += current.value

        while i < 2000:
            current = current.right
            i += 1
        result += current.value

        while i < 3000:
            current = current.right
            i += 1
        result += current.value

        return result


def parse_input():
    linked_list = CircularLinkedList(value=None, left=None, right=None)
    with (open(INPUT_FILE)) as input_file:
        for line in input_file:
            linked_list.add_node(value=int(line.strip()))

    return linked_list


def parse_input_2():
    DECRYPTION_KEY = 811589153
    linked_list = CircularLinkedList(value=None, left=None, right=None)
    with (open(INPUT_FILE)) as input_file:
        for line in input_file:
            linked_list.add_node(value=int(line.strip()) * DECRYPTION_KEY)

    return linked_list


def part_1(lst):
    to_move = []
    lst_copy = copy.copy(lst)

    to_move.append(lst_copy)
    lst_copy = lst_copy.right
    while not lst_copy.is_first:
        to_move.append(lst_copy)
        lst_copy = lst_copy.right

    for i in range(len(to_move)):
        left = to_move[i].remove_node()
        to_move[i] = left.insert_node(
            index=to_move[i].value, value=to_move[i].value)

    return to_move[0].get_grove_coords_sum()


def part_2(lst):
    to_move = []
    lst_copy = copy.copy(lst)

    to_move.append(lst_copy)
    lst_copy = lst_copy.right
    while not lst_copy.is_first:
        to_move.append(lst_copy)
        lst_copy = lst_copy.right

    for _ in range(10):
        for i in range(len(to_move)):
            left = to_move[i].remove_node()
            to_move[i] = left.insert_node(
                index=to_move[i].value, value=to_move[i].value)

    return to_move[0].get_grove_coords_sum()


if __name__ == "__main__":
    linked_list = parse_input()
    result_1 = part_1(linked_list)
    print("Part 1: ", result_1)

    linked_list = parse_input_2()
    result_2 = part_2(linked_list)
    print("Part 2: ", result_2)

import math


class Test:
    def __init__(self, divisible_by, success_id, fail_id):
        self.divisible_by = divisible_by
        self.success_id = success_id
        self.fail_id = fail_id


class Operation:
    def __init__(self, type, number):
        self.type = type
        self.number = number


class Monkey:
    def __init__(self, id, items, operation, test, inspected):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.inspected = inspected


def parse_input():
    monkeys = []
    id = 0
    items = []
    operation = None
    test = None
    divisible_by = None
    success_id = None
    fail_id = None
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_strip = line.strip()
            if len(line_strip) == 0:
                id += 1
                items = []
                operation = None
                test = None
                divisible_by = None
                success_id = None
                fail_id = None
                continue

            line_split = line_strip.split(':')
            if line_split[0].strip().startswith("Monkey"):
                continue
            elif line_split[0].strip().startswith("Starting items"):
                items_str = line_split[1].strip().split(', ')
                items = [int(number_as_string)
                         for number_as_string in items_str]
            elif line_split[0].strip().startswith("Operation"):
                operation_split = line_split[1].strip().split()
                operation_type = operation_split[3]
                operation_number = operation_split[4]
                operation = Operation(
                    type=operation_type, number=operation_number)
            elif line_split[0].strip().startswith("Test"):
                divisible_by = int(line_split[1].strip().split()[2])
            elif line_split[0].strip().startswith("If true"):
                success_id = int(line_split[1].strip().split()[3])
            elif line_split[0].strip().startswith("If false"):
                fail_id = int(line_split[1].strip().split()[3])
                test = Test(divisible_by, success_id, fail_id)
                monkeys.append(Monkey(id, items, operation, test, inspected=0))

    return monkeys


def part_1(monkeys):
    for _ in range(20):
        for monkey in monkeys:
            items = monkey.items
            operation = monkey.operation
            test = monkey.test

            for item in items:
                new = None
                number = None
                if operation.number == "old":
                    number = item
                else:
                    number = int(operation.number)
                if operation.type == "+":
                    new = item + number
                elif operation.type == "*":
                    new = item * number

                worry = math.floor(new / 3)
                if worry % test.divisible_by == 0:
                    monkeys[test.success_id].items.append(worry)
                else:
                    monkeys[test.fail_id].items.append(worry)

            monkey.inspected += len(items)
            monkey.items = []

    monkeys.sort(key=lambda monkey: monkey.inspected, reverse=True)
    result = 1
    for i in range(2):
        result *= monkeys[i].inspected

    return result


class Item:
    def __init__(self, modulos):
        self.modulos = modulos


def transform_monkeys_for_part_2(monkeys):
    modulos = set()
    for monkey in monkeys:
        modulos.add(monkey.test.divisible_by)

    for monkey in monkeys:
        new_items = []
        for item in monkey.items:
            new_item_modulos = {}
            for modulo in modulos:
                new_item_modulos[str(modulo)] = item % modulo
            new_items.append(Item(modulos=new_item_modulos))
        monkey.items = new_items

    return monkeys


def remainder_to_smallest_possible(value, modulo):
    if value >= int(modulo):
        return value % int(
            modulo)
    return value


def get_new_modulos_add(modulos, add_number):
    new_modulos = {}
    for modulo in modulos:
        new_remainder = modulos[modulo] + add_number
        new_modulos[modulo] = remainder_to_smallest_possible(
            value=new_remainder, modulo=modulo)
    return new_modulos


def get_new_modulos_multiply(modulos, multiply_number):
    new_modulos = {}
    for modulo in modulos:
        new_remainder = None
        if multiply_number is None:
            new_remainder = modulos[modulo] * modulos[modulo]
        else:
            new_remainder = modulos[modulo] * multiply_number
        new_modulos[modulo] = remainder_to_smallest_possible(
            value=new_remainder, modulo=modulo)
    return new_modulos


def part_2(monkeys):
    monkeys = transform_monkeys_for_part_2(monkeys)
    for i in range(10000):
        for monkey in monkeys:
            items = monkey.items
            operation = monkey.operation
            test = monkey.test

            for item in items:
                modulos = item.modulos
                number = None if operation.number == "old" else int(
                    operation.number)

                item_to_throw = None
                new_modulos = {}
                if operation.type == "+":
                    new_modulos = get_new_modulos_add(
                        modulos, add_number=number)
                elif operation.type == "*":
                    new_modulos = get_new_modulos_multiply(
                        modulos, multiply_number=number)

                item_to_throw = Item(modulos=new_modulos)

                if item_to_throw.modulos[str(test.divisible_by)] == 0:
                    monkeys[test.success_id].items.append(item_to_throw)
                else:
                    monkeys[test.fail_id].items.append(item_to_throw)

            monkey.inspected += len(items)
            monkey.items = []

    monkeys.sort(key=lambda monkey: monkey.inspected, reverse=True)
    result = 1
    for i in range(2):
        result *= monkeys[i].inspected

    return result


if __name__ == "__main__":
    monkeys = parse_input()

    result_1 = part_1(monkeys)
    print("Part 1: ", result_1)

    monkeys = parse_input()
    result_2 = part_2(monkeys)
    print("Part 2: ", result_2)

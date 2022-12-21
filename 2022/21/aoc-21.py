import sympy


class OperationMonkey:
    def __init__(self, name, operation, operands):
        self.name = name
        self.operation = operation
        self.operands = operands


class NumberMonkey:
    def __init__(self, name, value):
        self.name = name
        self.value = value


INPUT_FILE = "./input.txt"


def parse_input():
    monkeys = {}
    with (open(INPUT_FILE)) as input_file:
        for line in input_file:
            line_strip = line.strip()
            line_split_colon = line_strip.split(": ")
            name = line_split_colon[0]
            operation_split = line_split_colon[1].split()

            if len(operation_split) == 1:
                monkey = NumberMonkey(name, value=int(operation_split[0]))
                monkeys[name] = monkey
            else:
                operands = [operation_split[0], operation_split[2]]
                operation = operation_split[1]
                monkey = OperationMonkey(name, operation, operands)
                monkeys[name] = monkey

    return monkeys


def parse_input_2():
    monkeys = {}
    with (open(INPUT_FILE)) as input_file:
        for line in input_file:
            line_strip = line.strip()
            line_split_colon = line_strip.split(": ")
            name = line_split_colon[0]
            operation_split = line_split_colon[1].split()

            if len(operation_split) == 1:
                if name == "humn":
                    monkey = NumberMonkey(name, value="x")
                    monkeys[name] = monkey
                else:
                    monkey = NumberMonkey(name, value=int(operation_split[0]))
                    monkeys[name] = monkey
            else:
                operands = [operation_split[0], operation_split[2]]
                operation = operation_split[1]
                monkey = OperationMonkey(name, operation, operands)
                monkeys[name] = monkey

    return monkeys


def get_monkey_value(monkeys, name):
    monkey = monkeys[name]
    if isinstance(monkey, NumberMonkey):
        return monkey.value

    if monkey.operation == "+":
        return get_monkey_value(monkeys, monkey.operands[0]) + get_monkey_value(monkeys, monkey.operands[1])
    if monkey.operation == "-":
        return get_monkey_value(monkeys, monkey.operands[0]) - get_monkey_value(monkeys, monkey.operands[1])
    if monkey.operation == "*":
        return get_monkey_value(monkeys, monkey.operands[0]) * get_monkey_value(monkeys, monkey.operands[1])
    if monkey.operation == "/":
        return get_monkey_value(monkeys, monkey.operands[0]) / get_monkey_value(monkeys, monkey.operands[1])

    return None


def get_monkey_expr(monkeys, name):
    monkey = monkeys[name]
    if isinstance(monkey, NumberMonkey):
        return str(monkey.value)

    if monkey.operation == "+":
        return "(" + get_monkey_expr(monkeys, monkey.operands[0]) + "+" + get_monkey_expr(monkeys, monkey.operands[1]) + ")"
    if monkey.operation == "-":
        return "(" + get_monkey_expr(monkeys, monkey.operands[0]) + "-" + get_monkey_expr(monkeys, monkey.operands[1]) + ")"
    if monkey.operation == "*":
        return "(" + get_monkey_expr(monkeys, monkey.operands[0]) + "*" + get_monkey_expr(monkeys, monkey.operands[1]) + ")"
    if monkey.operation == "/":
        return "(" + get_monkey_expr(monkeys, monkey.operands[0]) + "/" + get_monkey_expr(monkeys, monkey.operands[1]) + ")"

    return None


def part_1(monkeys):
    return get_monkey_value(monkeys, "root")


def part_2(monkeys):
    operand_1 = monkeys["root"].operands[0]
    operand_2 = monkeys["root"].operands[1]
    expr_1 = get_monkey_expr(monkeys, operand_1)
    expr_2 = get_monkey_expr(monkeys, operand_2)

    sympy_eq = sympy.sympify("Eq(" + expr_1 + "," + expr_2 + ")")
    solution = sympy.solve(sympy_eq)[0]
    return solution


if __name__ == "__main__":
    monkeys = parse_input()
    result_1 = part_1(monkeys)
    print("Part 1: ", result_1)

    monkeys = parse_input_2()
    result_2 = part_2(monkeys)
    print("Part 2: ", result_2)

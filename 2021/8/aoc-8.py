class Signal:
    def __init__(self, patterns, output):
        self.patterns = patterns
        self.output = output


def get_signals():
    signals = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            line_split = line.split(" | ")
            patterns = line_split[0].split()
            patterns_sorted = []
            for pattern in patterns:
                patterns_sorted.append(''.join(sorted(pattern)))
            output = line_split[1].split()
            output_sorted = []
            for digit in output:
                output_sorted.append(''.join(sorted(digit)))
            signal = Signal(patterns_sorted, output_sorted)
            signals.append(signal)

    return signals


def is_unique_digit(digit):
    return len(digit) == 2 or len(digit) == 3 or len(digit) == 4 or len(digit) == 7


def count_simple_digits(signals):
    unique_count = 0
    for signal in signals:
        output = signal.output
        for digit in output:
            if is_unique_digit(digit):
                unique_count += 1

    return unique_count


def init_signal_mappings():
    return {"a": None, "b": None, "c": None, "d": None, "e": None, "f": None, "g": None}


def init_digits():
    return {"0": None, "1": None, "2": None, "3": None, "4": None, "5": None, "6": None, "7": None, "8": None, "9": None}


def find_unique_digit(patterns, with_char_count):
    for pattern in patterns:
        if len(pattern) == with_char_count:
            return pattern


# def find_two(patterns, one):
#     missing_c = []
#     missing_f = []
#     for pattern in patterns:
#       for char in one:
#         if char not in pattern


# def find_five(one, patterns):
#     for pattern in patterns:


def find_zero(patterns, digits):
    for pattern in patterns:
        if len(pattern) == 6:
            contains_seven = True
            for char in digits["7"]:
                if char not in pattern:
                    contains_seven = False
            if contains_seven and pattern != digits["9"]:
                return pattern


def find_two(patterns, mappings):
    for pattern in patterns:
        if len(pattern) == 5 and mappings["c"] in pattern and mappings["f"] not in pattern:
            return pattern


def find_three(patterns, mappings):
    for pattern in patterns:
        if len(pattern) == 5 and mappings["c"] in pattern and mappings["f"] in pattern:
            return pattern


def find_five(patterns, mappings):
    for pattern in patterns:
        if len(pattern) == 5 and mappings["c"] not in pattern and mappings["f"] in pattern:
            return pattern


def find_six(patterns, digits):
    for pattern in patterns:
        if len(pattern) == 6 and pattern != digits["0"] and pattern != digits["9"]:
            return pattern


def find_nine(patterns, four):
    for pattern in patterns:
        if len(pattern) == 6:
            contains_four = True
            for char in four:
                if char not in pattern:
                    contains_four = False
            if contains_four:
                return pattern


def map_a(one, seven):
    for char in seven:
        if char not in one:
            return char


def map_c(one, six):
    for char in one:
        if char not in six:
            return char


def map_f(one, mappings):
    for char in one:
        if char != mappings["c"]:
            return char


def digits_to_decimal(digits):
    number_as_string = ''.join(digits)
    return int(number_as_string)


def part_2(signals):
    signal_mappings = init_signal_mappings()
    digits = init_digits()
    sum_of_outputs = 0

    for signal in signals:
        patterns = signal.patterns
        # must be in this order
        digits["1"] = find_unique_digit(patterns, with_char_count=2)
        digits["4"] = find_unique_digit(patterns, with_char_count=4)
        digits["7"] = find_unique_digit(patterns, with_char_count=3)
        digits["8"] = find_unique_digit(patterns, with_char_count=7)
        digits["9"] = find_nine(patterns, four=digits["4"])
        digits["0"] = find_zero(patterns, digits)
        digits["6"] = find_six(patterns, digits)
        signal_mappings["a"] = map_a(digits["1"], digits["7"])
        signal_mappings["c"] = map_c(digits["1"], digits["6"])
        signal_mappings["f"] = map_f(digits["1"], signal_mappings)
        digits["2"] = find_two(patterns, signal_mappings)
        digits["3"] = find_three(patterns, signal_mappings)
        digits["5"] = find_five(patterns, signal_mappings)

        output = signal.output
        real_digits = []
        for digit in output:
            real_digit = list(digits.keys())[
                list(digits.values()).index(digit)]
            real_digits.append(real_digit)

        sum_of_outputs += digits_to_decimal(real_digits)

    return sum_of_outputs


if __name__ == "__main__":
    signals = get_signals()
    unique_count = count_simple_digits(signals)
    print("Digits 1, 4, 7 or 8 appear ", unique_count, " times.")
    sum_of_outputs = part_2(signals)
    print("Sum of outputs: ", sum_of_outputs)

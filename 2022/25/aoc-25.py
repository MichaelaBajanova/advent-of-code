def parse_input():
    snafu_nums = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            snafu_nums.append(line.strip())

    return snafu_nums


def parse_snafu_digit(digit):
    if digit in ['0', '1', '2']:
        return int(digit)
    elif digit == '-':
        return -1
    elif digit == '=':
        return -2


def snafu_to_decimal(snafu):
    reversed = snafu[::-1]
    decimal = 0
    for i in range(len(reversed)):
        num = parse_snafu_digit(reversed[i])
        decimal += num * pow(5, i)
    return decimal


def decimal_to_snafu(decimal):
    tmp_decimal = decimal
    snafu = ""
    while tmp_decimal > 0:
        rem = tmp_decimal % 5
        tmp_decimal = tmp_decimal // 5
        if rem <= 2:
            snafu += str(rem)
        elif rem == 3:
            snafu += "="
            tmp_decimal += 1
        elif rem == 4:
            snafu += "-"
            tmp_decimal += 1
    return snafu[::-1]


def part_1(snafu_nums):
    decimal_sum = 0
    for snafu in snafu_nums:
        decimal_sum += snafu_to_decimal(snafu)

    return decimal_to_snafu(decimal_sum)


def part_2(snafu_nums):
    result = 0
    return result


if __name__ == "__main__":
    snafu_nums = parse_input()

    result_1 = part_1(snafu_nums)
    print("Part 1: ", result_1)
    result_2 = part_2(snafu_nums)
    print("Part 2: ", result_2)

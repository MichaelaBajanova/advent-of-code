def get_report():
    report = []
    with (open("./input.txt")) as input_file:
        for line in input_file:
            report.append(line)

    return report


def transpose_matrix(matrix):
    result = []
    for _ in range(len(matrix[0]) - 1):
        result.append([])

    for row in matrix:
        for i in range(len(row) - 1):
            result[i].append(row[i])

    return result


def get_most_used(bits):
    one_count = 0
    for bit in bits:
        if bit == "1":
            one_count += 1

    if one_count >= len(bits) - one_count:
        return "1"
    else:
        return "0"


def get_least_used(bits):
    one_count = 0
    for bit in bits:
        if bit == "1":
            one_count += 1

    if one_count < len(bits) - one_count:
        return "1"
    else:
        return "0"


def simple(matrix):
    gamma = ""
    for row in matrix:
        gamma += get_most_used(row)

    epsilon = ""
    for bit in gamma:
        if bit == "0":
            epsilon += "1"
        else:
            epsilon += "0"

    print("Gamma: ", gamma)
    print("Epsilon: ", epsilon)


def advanced(report):
    oxygen_generator_report_copy = report[:]
    co2_scrubber_report_copy = report[:]
    for i in range(len(report[0]) - 1):
        if len(oxygen_generator_report_copy) > 1:
            transposed_oxygen = transpose_matrix(oxygen_generator_report_copy)
            most_used = get_most_used(transposed_oxygen[i])
            filtered_oxygen = list(filter(
                lambda code: code[i] == most_used, oxygen_generator_report_copy))
            oxygen_generator_report_copy = filtered_oxygen[:]

        if len(co2_scrubber_report_copy) > 1:
            transposed_co2 = transpose_matrix(co2_scrubber_report_copy)
            least_used = get_least_used(transposed_co2[i])
            filtered_co2 = list(filter(
                lambda code: code[i] == least_used, co2_scrubber_report_copy))
            co2_scrubber_report_copy = filtered_co2[:]

    print("Oxygen generator rating: ", oxygen_generator_report_copy)
    print("CO2 scrubber rating: ", co2_scrubber_report_copy)


if __name__ == "__main__":
    report = get_report()
    transposed_report = transpose_matrix(report)
    simple(transposed_report)
    advanced(report)

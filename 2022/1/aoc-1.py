def get_calories():
    calories = []
    with (open("./input.txt")) as input_file:
        elf_calories = 0
        for line in input_file:
            if line.strip() == "":
                calories.append(elf_calories)
                elf_calories = 0
            else:
                elf_calories += int(line.strip())

    return calories


def get_max_calories(calories):
    max = 0
    for calorie in calories:
        if calorie > max:
            max = calorie

    return max


def get_top_three_total(calories):
    sorted_calories = sorted(calories, reverse=True)
    total = 0
    for i in range(0, 3):
        total += sorted_calories[i]

    return total


if __name__ == "__main__":
    calories = get_calories()
    max_calories = get_max_calories(calories)
    print("Max calories: ", max_calories)
    total = get_top_three_total(calories)
    print("Total of top 3: ", total)

def get_positions():
    with (open("./input.txt")) as input_file:
        return [int(position) for position in input_file.readline().split(",")]


def get_fuel_amount_between_positions(positionFrom, positionTo):
    difference = abs(positionFrom - positionTo)
    # vzorec na sucet aritmetickej postupnosti
    return ((1 + difference) * difference) / 2


def simple(positions):
    fuels = []
    for position_to_align in positions:
        fuel = 0
        for current_position in positions:
            fuel += abs(position_to_align - current_position)
        fuels.append(fuel)

    min_fuel = fuels[0] if len(fuels) > 0 else 0
    for fuel in fuels:
        if fuel < min_fuel:
            min_fuel = fuel

    print("Fuel: ", min_fuel)


def advanced(positions):
    max_position = 0
    for position in positions:
        if position > max_position:
            max_position = position

    fuels = []
    for position_to_align in range(1, max_position + 1):
        fuel = 0
        for current_position in positions:
            fuel += get_fuel_amount_between_positions(
                positionFrom=current_position, positionTo=position_to_align)
        fuels.append(fuel)

    min_fuel = fuels[0] if len(fuels) > 0 else 0
    for fuel in fuels:
        if fuel < min_fuel:
            min_fuel = fuel

    print("Fuel: ", min_fuel)


if __name__ == "__main__":
    positions = get_positions()
    simple(positions)
    advanced(positions)

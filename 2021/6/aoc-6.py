def get_timers():
    with (open("./input.txt")) as input_file:
        return [int(timer) for timer in input_file.readline().split(",")]


# very slow
def after_80_days(timers):
    timers_copy = timers[:]
    for _ in range(80):
        for i in range(len(timers_copy)):
            if timers_copy[i] == 0:
                timers_copy.append(8)
                timers_copy[i] = 6
            else:
                timers_copy[i] -= 1
    print(len(timers_copy))


def after_256_days(timers):
    histogram = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0}
    # initialize histogram
    for timer in timers:
        histogram[timer] += 1

    for _ in range(256):
        new_fish = histogram[0]
        for i in range(8):
            histogram[i] = histogram[i + 1]
        histogram[8] = new_fish
        histogram[6] += new_fish

    count = 0
    for i in range(9):
        count += histogram[i]
    print(count)


if __name__ == "__main__":
    timers = get_timers()
    after_80_days(timers)
    after_256_days(timers)

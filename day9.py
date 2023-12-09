def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]

    sum_of_nexts = 0
    for line in input_lines:
        level_0 = [int(n) for n in line.split(" ")]
        levels = [level_0]
        while any(n != 0 for n in levels[-1]):
            levels.append([
                levels[-1][i + 1] - levels[-1][i] for i in range(len(levels[-1]) - 1)
            ])
        # iterate backwards on levels by index
        levels[-1].append(0)
        for i in range(1, len(levels)):
            next_one = levels[-i][-1] + levels[-1 - i][-1]
            levels[-1 - i].append(next_one)
        sum_of_nexts += levels[0][-1]
    print(sum_of_nexts)  # 2008960228

    # now do it backwards
    # by reversing input lines one by one
    sum_of_nexts = 0
    for line in input_lines:
        level_0 = [int(n) for n in reversed(line.split(" "))]
        levels = [level_0]
        while any(n != 0 for n in levels[-1]):
            levels.append([
                levels[-1][i + 1] - levels[-1][i] for i in range(len(levels[-1]) - 1)
            ])
        # iterate backwards on levels by index
        levels[-1].append(0)
        for i in range(1, len(levels)):
            next_one = levels[-i][-1] + levels[-1 - i][-1]
            levels[-1 - i].append(next_one)
        sum_of_nexts += levels[0][-1]
    print(sum_of_nexts)  # 1097


if __name__ == '__main__':
    main()

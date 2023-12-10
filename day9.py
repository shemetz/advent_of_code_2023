from typing import List

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


def extrapolate_next_value(sequence: List[int]) -> int:
    levels = [sequence]
    while any(n != 0 for n in levels[-1]):
        levels.append([
            levels[-1][i + 1] - levels[-1][i] for i in range(len(levels[-1]) - 1)
        ])
    # iterate backwards on levels by index
    levels[-1].append(0)
    for i in range(1, len(levels)):
        next_one = levels[-i][-1] + levels[-1 - i][-1]
        levels[-1 - i].append(next_one)
    return levels[0][-1]


sum_of_nexts = sum(extrapolate_next_value([int(n) for n in line.split(" ")]) for line in input_lines)
print(sum_of_nexts)  # 2008960228

# now extrapolate backwards, by just extrapolating forwards on reversed sequences
sum_of_prevs = sum(extrapolate_next_value([int(n) for n in reversed(line.split(" "))]) for line in input_lines)
print(sum_of_prevs)  # 1097

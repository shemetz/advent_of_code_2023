import re
from collections import defaultdict

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]
grid = input_lines
height = len(grid)
width = len(grid[0])
sum_nums = 0
gear_counts = defaultdict(list)
for row, line in enumerate(grid):
    # e.g. ..35.$633.
    for match in re.finditer(r'\d+', line):
        c_from, c_to = match.start(), match.end()
        part_number = match.group()
        is_part = False
        for c in range(c_from - 1, c_to + 1):
            if 0 <= c < width:
                for r in range(row - 1, row + 2):
                    if 0 <= r < height:
                        if grid[r][c] != '.' and not grid[r][c].isdigit():
                            is_part = True
                            if grid[r][c] == "*":
                                gear_counts[(r, c)].append(part_number)
        if is_part:
            sum_nums += int(part_number)
print(sum_nums)  # 527369

sum_gear_ratios = 0
for gear_r_c, parts in gear_counts.items():
    if len(parts) == 2:
        sum_gear_ratios += int(parts[0]) * int(parts[1])

print(sum_gear_ratios)  # 73074886

from collections import deque

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

grid = [list(line) for line in input_lines]
height, width = len(grid), len(grid[0])
assert width == height  # 11 in example, 131 in real input
start = None
for r in range(height):
    for c in range(width):
        if grid[r][c] == 'S':
            start = (r, c)


def get_neighbors(r, c):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width and grid[nr][nc] != '#':
            neighbors.append((nr, nc))
    return neighbors


frontier = deque([(-1, start)])
visited_odd = set()
visited_even = set()
MAX_STEP_COUNT = 64
while frontier:
    step_count, (r, c) = frontier.popleft()
    step_count += 1
    if step_count > MAX_STEP_COUNT:
        continue
    if step_count % 2 == 1:
        if (r, c) in visited_odd:
            continue
        visited_odd.add((r, c))
    else:
        if (r, c) in visited_even:
            continue
        visited_even.add((r, c))
    for nr, nc in get_neighbors(r, c):
        frontier.append((step_count, (nr, nc)))

print(len(visited_even))  # 3743

# PART 2 - geometric solution based on https://github.com/villuna/aoc23/wiki/A-Geometric-solution-to-advent-of-code-2023,-day-21
# (I didn't manage to solve this myself)

MAX_STEP_COUNT = 26501365
half_width = width // 2  # note:  this is rounded down!
extra_squares_each_side = (MAX_STEP_COUNT - half_width) // width

frontier = deque([(-1, start)])
visited_odd = set()
visited_even = set()
MAX_STEP_COUNT = width * 4  # = full
while frontier:
    step_count, (r, c) = frontier.popleft()
    step_count += 1
    if step_count > MAX_STEP_COUNT:
        continue
    if step_count % 2 == 1:
        if (r, c) in visited_odd:
            continue
        visited_odd.add((r, c))
    else:
        if (r, c) in visited_even:
            continue
        visited_even.add((r, c))
    for nr, nc in get_neighbors(r, c):
        frontier.append((step_count, (nr, nc)))

frontier = deque([(-1, (0, 0)), (-1, (width - 1, 0)), (-1, (0, width - 1)), (-1, (width - 1, width - 1))])
visited_odd_from_corners = set((r, c) for r, c in visited_odd if abs(r-start[0] + c-start[1]) >= half_width)
visited_even_from_corners = set((r, c) for r, c in visited_even if abs(r-start[0] + c-start[1]) >= half_width)
l_v_o = len(visited_odd)
l_v_e = len(visited_even)
l_v_o_c = len(visited_odd_from_corners)
l_v_e_c = len(visited_even_from_corners)
print(f"l_v_o = {l_v_o}; l_v_e = {l_v_e}; l_v_o_c = {l_v_o_c}; l_v_e_c = {l_v_e_c}")
n = extra_squares_each_side
ans_2 = ((n+1)*(n+1)) * l_v_o + (n*n) * l_v_e - (n+1) * l_v_o_c + n * l_v_e_c
print(ans_2)  #
# 618261389928641 WRONG
# 618261416632373 WRONG
# needs to be between:
# 618261400000000
# 618273615815477

# 618261433219147 is the true answer
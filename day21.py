from collections import deque

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

grid = [list(line) * 99 for line in input_lines * 99]
height, width = len(grid), len(grid[0])
assert width == height  # 11 in example, 131 in real input
start = None
for r in range(height):
    for c in range(width):
        if grid[r][c] == 'S':
            start = (r, c)
start = (width//2, height//2)


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
MAX_STEP_COUNT = 501
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

# # print grid
# for r in range(height):
#     for c in range(width):
#         if (r, c) in visited_even:
#             print('E', end='')
#         else:
#             print(grid[r][c], end='')
#     print()

cycle_size = 11 * 2


def get_neighbors_2(r, c):
    neighbors = []
    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if grid[nr % height][nc % width] != '#':
            neighbors.append((nr, nc))
    return neighbors


# MAX_STEP_COUNT = 26501365
MAX_STEP_COUNT = 501
curr_frontier = [start]
visited_odd = set()
accumulated_numbers = []
step = 0
while step < cycle_size * 10:
    step += 1
    next_frontier = []
    for r, c in curr_frontier:
        if step % 2 == 1:
            if (r, c) in visited_odd:
                continue
            visited_odd.add((r, c))
        for nr, nc in get_neighbors_2(r, c):
            next_frontier.append((nr, nc))
    curr_frontier = next_frontier
    if step % 2 == 1:
        accumulated_numbers.append(len(visited_odd))
        if len(accumulated_numbers) > cycle_size * 2:
            if step % cycle_size == MAX_STEP_COUNT % cycle_size:
                acceleration = (accumulated_numbers[-1] - accumulated_numbers[-1 - cycle_size]) - (
                        accumulated_numbers[-2] - accumulated_numbers[-2 - cycle_size])
                assert accumulated_numbers[-1] == acceleration + accumulated_numbers[-1 - cycle_size] + \
                       accumulated_numbers[-2] - accumulated_numbers[-2 - cycle_size]
                cycles_so_far = step // cycle_size
                leftover_cycles = (MAX_STEP_COUNT - step) // cycle_size
                print(f"step: {step}    acceleration: {acceleration}, cycles: {cycles_so_far}, leftover: {leftover_cycles}")
                print(f"a_n-c = {accumulated_numbers[-1 - cycle_size]}")
                print(f"a_n = {accumulated_numbers[-1]}")
                print(f"acc*cyc = {acceleration * cycles_so_far}")
                # value_by_formula = accumulated_numbers[-1 - cycle_size] - 44 + \
                #                    acceleration * cycles_so_far * 18 ** 2 // 10 ** 2
                value_by_formula = accumulated_numbers[-1 - cycle_size] - 44 + acceleration * cycles_so_far * 103
                print(accumulated_numbers[-1] - value_by_formula)
                # assert accumulated_numbers[-1] == value_by_formula
                # answer = accumulated_numbers[-1] - 44 + acceleration * leftover_cycles * 36 ** 2 // 10 ** 2
                # print(answer)
                # break

                # a_n = acceleration a_{n-1} + a_{n-c} - a_{n-c-1}
                # leftover_increase = leftover_cycles * acceleration
                # total = accumulated_numbers[-1] + leftover_increase
                # print(f"total: {total}")
                # (I made sure it really cycles from here via trial and error)
                # break


# attempt 2
# x = 7 + 101143
# y = 60428 * x**2 + 30006 * x + 3743
print("not", 618261391140643)  # 618261391140643 is TOO LOW
print("not", 618261400000000)  # 618261400000000 is TOO LOW
# (same as above but x + 1, to clamp it)
print("not", 618273615815477)  # 618273615815477 is TOO HIGH

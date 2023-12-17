import heapq

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

width, height = len(input_lines[0]), len(input_lines)
grid = {}
for y in range(height):
    for x in range(width):
        grid[x, y] = int(input_lines[y][x])


def solve(part: int):
    frontier = [(0, 0, 0, None, 0)]  # accumulated cost, x, y, direc, dist_in_direc
    visited_costs = {}
    while frontier:
        cost, x, y, direc, dist_in_direc = heapq.heappop(frontier)
        if (x, y) == (width - 1, height - 1):
            if part == 2 and dist_in_direc < 4:
                continue
            return cost
        if visited_costs.get((x, y, direc, dist_in_direc), 999999) <= cost:
            continue
        visited_costs[(x, y, direc, dist_in_direc)] = cost
        for new_direc, (dx, dy) in enumerate([(0, 1), (1, 0), (0, -1), (-1, 0)]):
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) not in grid:
                continue  # can't move off the grid
            if (new_direc + 2) % 4 == direc:
                continue  # can't turn back
            if new_direc != direc:
                if part == 2 and direc is not None and dist_in_direc < 4:
                    continue  # minimum of 4 steps forward at a time
                new_d_i_d = 1
            else:
                new_d_i_d = dist_in_direc + 1
            if part == 1 and new_d_i_d >= 4:
                continue  # can't move straight for 4+ steps
            if part == 2 and new_d_i_d >= 11:
                continue  # can't move straight for 11+ steps
            heapq.heappush(frontier, (cost + grid[new_x, new_y], new_x, new_y, new_direc, new_d_i_d))
    print("NO SOLUTION FOUND")


final_cost = solve(1)
print(final_cost)  # 698

final_cost = solve(2)
print(final_cost)  # 825

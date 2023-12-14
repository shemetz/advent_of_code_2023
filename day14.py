from functools import cache

import numpy as np

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

starting_grid = [list(line) for line in input_lines]
# starting_grid = np.array([list(line) for line in input_lines])
height, width = len(starting_grid), len(starting_grid[0])
# height, width = starting_grid.shape


# print("\n".join(map("".join, grid)))  # pretty print 2d character grid

def tupled(grid):
    return tuple(tuple(line) for line in grid)


@cache
def tilted_north(grid):
    next_grid = [["." for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "#":
                next_grid[y][x] = "#"
            elif grid[y][x] == "O":
                first_empty_y_above = y
                while first_empty_y_above >= 0 and next_grid[first_empty_y_above][x] == ".":
                    first_empty_y_above -= 1
                first_empty_y_above += 1
                next_grid[first_empty_y_above][x] = "O"
    return next_grid


def calc_load(grid):
    total_load = 0
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "O":
                total_load += height - y
    return total_load


print(calc_load(tilted_north(tupled(starting_grid))))  # Part 1:  109661


def iterate(grid):
    for j in range(4):
        # tilt
        grid = tupled(tilted_north(grid))
        # rotate clockwise
        grid = zip(*grid[::-1])
        # make tuple
        grid = tupled(grid)
    return grid


def iter_until_loop():
    seen_states = []
    grid = tupled(starting_grid)
    while True:
        if grid in seen_states:
            loop_start = seen_states.index(grid)
            loop_length = len(seen_states) - loop_start
            return loop_start, loop_length, seen_states
        seen_states.append(grid)
        grid = iterate(grid)


big_n = 1000000000
loop_start, loop_length, seen_states = iter_until_loop()
n = (big_n - loop_start) % loop_length
last_state = seen_states[loop_start + n]
print(calc_load(last_state))  # Part 2:  90176

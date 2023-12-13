from itertools import groupby
import numpy as np

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

# split by empty lines
grids = [list(g) for k, g in groupby(input_lines, lambda l: l == "") if not k]
# convert into numpy arrays
grids = [np.array([list(row) for row in grid]) for grid in grids]


def find_mirror_reflection_lines(grid, ignore_y=None, ignore_x=None):
    # row by row with indices
    height, width = grid.shape
    mirror_y, mirror_x = 0, 0
    for y in range(1, height):
        if y == ignore_y:
            continue
        if y > height // 2:
            invy = height - y
            subgrid_from_y = grid[y:, :]
            same_size_subgrid_until_y = grid[y - invy:y, :]
        else:
            subgrid_from_y = grid[y:2 * y, :]
            same_size_subgrid_until_y = grid[:y, :]
        flip_shadow = np.flip(same_size_subgrid_until_y, 0)
        if np.all(subgrid_from_y == flip_shadow):
            mirror_y = y
            break
    # repeat with x
    for x in range(1, width):
        if x == ignore_x:
            continue
        if x > width // 2:
            invx = width - x
            subgrid_from_x = grid[:, x:]
            same_size_subgrid_until_x = grid[:, x - invx:x]
        else:
            subgrid_from_x = grid[:, x:2 * x]
            same_size_subgrid_until_x = grid[:, :x]
        flip_shadow = np.flip(same_size_subgrid_until_x, 1)
        if np.all(subgrid_from_x == flip_shadow):
            mirror_x = x
            break
    return mirror_y, mirror_x


summed_totals = 0
for grid in grids:
    sy, sx = find_mirror_reflection_lines(grid)
    summed_totals += sx + 100 * sy
print(summed_totals)  # 33975

summed_totals = 0
for grid in grids:
    sy, sx = find_mirror_reflection_lines(grid)
    # for each grid square, try to unsmudge it and see if it changes things
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            smudged_grid = grid.copy()
            smudged_grid[y, x] = "." if smudged_grid[y, x] == "#" else "#"
            ny, nx = find_mirror_reflection_lines(smudged_grid, sy, sx)
            if nx + ny > 0:
                summed_totals += nx + 100 * ny
                break
        else:
            continue
        break
    else:
        print("\n".join(map("".join, grid)))  # pretty print 2d character grid
        raise Exception("should not happen!")
print(summed_totals)  # 29083

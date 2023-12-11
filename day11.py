with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

grid = [[char for char in line] for line in input_lines]
height = len(grid)
width = len(grid[0])
for i in range(height - 1, -1, -1):
    if all(grid[i][j] == '.' for j in range(width)):
        grid.insert(i, ['+'] * width)
        height += 1
for j in range(width - 1, -1, -1):
    if all(grid[i][j] in '.+' for i in range(height)):
        for i in range(height):
            grid[i].insert(j, '+')
        width += 1

galaxies = []
for i in range(height):
    for j in range(width):
        if grid[i][j] == '#':
            galaxies.append((i, j))

# Part 1
total_distances = 0
for gi in range(len(galaxies)):
    for gi2 in range(gi + 1, len(galaxies)):
        i, j = galaxies[gi]
        i2, j2 = galaxies[gi2]
        distance = abs(i - i2) + abs(j - j2)
        total_distances += distance
print(total_distances)  # 9681886

# Part 2
empty_rs = [i for i in range(height) if grid[i][0] == '+']
empty_cs = [j for j in range(width) if grid[0][j] == '+']
print(empty_rs)
print(empty_cs)
total_distances = 0
for gi in range(len(galaxies)):
    for gi2 in range(gi + 1, len(galaxies)):
        i, j = galaxies[gi]
        i2, j2 = galaxies[gi2]
        distance = abs(i - i2) + abs(j - j2)
        empties = 0
        for mid_i in range(min(i, i2) + 1, max(i, i2)):
            if mid_i in empty_rs:
                empties += 1
        for mid_j in range(min(j, j2) + 1, max(j, j2)):
            if mid_j in empty_cs:
                empties += 1
        distance -= 2 * empties
        # distance += 1_0 * empties  # for example
        distance += 1_000_000 * empties
        total_distances += distance
print(total_distances)  # 791134099634

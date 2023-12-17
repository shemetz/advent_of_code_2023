import numpy as np

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

width, height = len(input_lines[0]), len(input_lines)
grid = np.array([[ch for ch in line] for line in input_lines], dtype=str)
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)


def solve(start_r, start_c, start_direction):
    energized = np.full((width, height), 0)
    visited = set()
    frontier = [(start_r, start_c, start_direction)]
    while frontier:
        r, c, direction = frontier.pop()
        # boundary check
        if r < 0 or r >= width or c < 0 or c >= height:
            continue
        if (r, c, direction) in visited:
            continue
        visited.add((r, c, direction))
        energized[r, c] = True
        # movement uninterrupted
        if (grid[r, c] == '.'
            or (grid[r, c] == "-" and direction in [LEFT, RIGHT])) \
                or (grid[r, c] == "|" and direction in [UP, DOWN]):
            next_direction = direction
        # split
        elif grid[r, c] == "-":  # (UP or DOWN)
            next_direction = LEFT
            frontier.append((r + next_direction[0], c + next_direction[1], next_direction))
            next_direction = RIGHT
        elif grid[r, c] == "|":  # (RIGHT or LEFT)
            next_direction = UP
            frontier.append((r + next_direction[0], c + next_direction[1], next_direction))
            next_direction = DOWN
        # bounce 90 degrees
        elif grid[r, c] == '/':
            if direction in [UP, RIGHT]:
                next_direction = UP if direction == RIGHT else RIGHT
            else:
                next_direction = DOWN if direction == LEFT else LEFT
        elif grid[r, c] == '\\':
            if direction in [UP, LEFT]:
                next_direction = LEFT if direction == UP else UP
            else:
                next_direction = RIGHT if direction != RIGHT else DOWN
        else:
            print("THIS SHOULD NOT HAPPEN")
            break
        frontier.append((r + next_direction[0], c + next_direction[1], next_direction))
    return sum(energized.flatten())


# part 1
print(solve(0, 0, RIGHT))  # 7632

# part 2 - just repeat from each direction and calc max
best_solution = -1
for r in range(height):
    best_solution = max(best_solution, solve(r, 0, RIGHT))
    best_solution = max(best_solution, solve(r, width - 1, LEFT))
for c in range(width):
    best_solution = max(best_solution, solve(0, c, DOWN))
    best_solution = max(best_solution, solve(height - 1, c, UP))
print(best_solution)  # 8023

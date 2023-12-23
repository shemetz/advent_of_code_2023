from collections import defaultdict

import numpy as np

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

# MAYBE USEFUL
width, height = len(input_lines[0]), len(input_lines)
grid = np.array([[ch for ch in line] for line in input_lines], dtype=str)
UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)

start = (0, 1)  # first open space in row
end = (height - 1, width - 2)  # last open space in row

# depth first to find longest path
stack = [[start]]
longest_path = []
while stack:
    path = stack.pop()
    curr_r, curr_c = path[-1]
    if curr_r == end[0] and curr_c == end[1]:
        if len(path) > len(longest_path):
            longest_path = path
        continue
    for dr, dc in [UP, RIGHT, DOWN, LEFT]:
        new_r, new_c = curr_r + dr, curr_c + dc
        if (new_r, new_c) in path:
            continue
        if new_r < 0 or new_r >= width or new_c < 0 or new_c >= height:
            continue
        if grid[new_r, new_c] == '#':
            continue
        if grid[new_r, new_c] in '^>v<':
            # ensure direction
            if grid[new_r, new_c] == '^' and dr != -1:
                continue
            if grid[new_r, new_c] == '>' and dc != 1:
                continue
            if grid[new_r, new_c] == 'v' and dr != 1:
                continue
            if grid[new_r, new_c] == '<' and dc != -1:
                continue
        stack.append(path + [(new_r, new_c)])

longest_path_length = len(longest_path) - 1  # subtract 1 for start
print(longest_path_length)  # 2394

# now optimized - with shortcutting some paths
simplified_graph = defaultdict(lambda: defaultdict(lambda: -1))  # {from: {to: length}

# REWRITING WITHOUT RECURSION
frontier = [[start]]
while frontier:
    curr_path = frontier.pop()
    curr = curr_path[-1]
    path_start = curr_path[0]
    path_end = curr_path[-1]
    path_length = len(curr_path) - 1
    if curr == end:
        simplified_graph[path_start][path_end] = max(path_length, simplified_graph[path_start][path_end])
        continue
    neighbors = []
    for dr, dc in [UP, RIGHT, DOWN, LEFT]:
        new_r, new_c = curr[0] + dr, curr[1] + dc
        if new_r < 0 or new_r >= width or new_c < 0 or new_c >= height:
            continue
        if grid[new_r, new_c] == '#':
            continue
        if (new_r, new_c) in curr_path:
            continue
        neighbors.append((new_r, new_c))
    if len(neighbors) == 1:
        # just extend existing path
        curr_path.append(neighbors[0])
        frontier.append(curr_path)
    if len(neighbors) >= 2:
        if path_end not in simplified_graph[path_start]:
            simplified_graph[path_start][path_end] = path_length
            for neighbor in neighbors:
                frontier.append([path_end, neighbor])
        else:
            simplified_graph[path_start][path_end] = max(path_length, simplified_graph[path_start][path_end])

# now we have a simplified graph
# we can dfs on it to find longest path again
stack = [[start]]
longest_path_length = -1
while stack:
    path = stack.pop()
    curr = path[-1]
    if curr == end:
        path_length = sum([simplified_graph[path[i]][path[i + 1]] for i in range(len(path) - 1)])
        if path_length > longest_path_length:
            longest_path_length = path_length
        continue
    for neighbor in simplified_graph[curr]:
        if neighbor in path:
            continue
        stack.append(path + [neighbor])

print(longest_path_length)  # 6554

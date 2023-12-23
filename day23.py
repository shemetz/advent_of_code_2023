from collections import defaultdict

import numpy as np

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

UP, RIGHT, DOWN, LEFT = (-1, 0), (0, 1), (1, 0), (0, -1)

width, height = len(input_lines[0]), len(input_lines)
grid = np.array([[ch for ch in line] for line in input_lines], dtype=str)
start = (0, next(c for c in range(width) if grid[0][c] == "."))  # open space in first row
end = (height - 1, next(c for c in range(width) if grid[height - 1][c] == "."))  # open space in last row


def simplify_graph(part: int):
    print(f"Part {part}: simplifying graph...")
    simplified_graph = defaultdict(lambda: defaultdict(lambda: -1))  # {from: {to: length}
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
            if (new_r, new_c) in curr_path:
                continue
            if grid[new_r, new_c] == '#':
                continue
            if part == 1:
                if grid[new_r, new_c] == '>' and dc != 1:
                    continue
                if grid[new_r, new_c] == 'v' and dr != 1:
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
    return simplified_graph


def find_longest_path_length(graph):
    print(f"Finding longest path...")
    stack = [[start]]
    longest_path_length = -1
    while stack:
        path = stack.pop()
        curr = path[-1]
        if curr == end:
            path_length = sum([graph[path[i]][path[i + 1]] for i in range(len(path) - 1)])
            if path_length > longest_path_length:
                longest_path_length = path_length
            continue
        for neighbor in graph[curr]:
            if neighbor in path:
                continue
            stack.append(path + [neighbor])
    return longest_path_length


simp_graph_1 = simplify_graph(1)
print(find_longest_path_length(simp_graph_1))  # 2394
simp_graph_2 = simplify_graph(2)
print(find_longest_path_length(simp_graph_2))  # 6554 (takes about a minute to run)

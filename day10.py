from collections import deque


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    dirs = {
        # all in (r, c) notation
        '|': ((-1, 0), (+1, 0)),
        '-': ((0, +1), (0, -1)),
        'L': ((-1, 0), (0, +1)),
        'J': ((-1, 0), (0, -1)),
        '7': ((+1, 0), (0, -1)),
        'F': ((+1, 0), (0, +1)),
        '.': (),
    }
    grid = [list(line) for line in input_lines]
    height = len(grid)
    width = len(grid[0])
    start_r_c = (-1, -1)
    for r in range(height):
        for c in range(width):
            if grid[r][c] == 'S':
                start_r_c = (r, c)
                break
    sr, sc = start_r_c
    visited = set()
    arms = deque()
    if (+1, 0) in dirs[grid[sr - 1][sc]]:
        arms.append((sr - 1, sc, sr, sc, 1))
    if (-1, 0) in dirs[grid[sr + 1][sc]]:
        arms.append((sr + 1, sc, sr, sc, 1))
    if (0, +1) in dirs[grid[sr][sc - 1]]:
        arms.append((sr, sc - 1, sr, sc, 1))
    if (0, -1) in dirs[grid[sr][sc + 1]]:
        arms.append((sr, sc + 1, sr, sc, 1))
    while arms:
        r, c, from_r, from_c, dist = arms.popleft()
        if r < 0 or r >= height or c < 0 or c >= width:
            continue
        if grid[r][c] == '.' or grid[r][c] == 'S':
            continue
        if (r, c) in visited:
            print(dist)  # 6754
            break
        visited.add((r, c))
        assert grid[r][c] in dirs
        for dr, dc in dirs[grid[r][c]]:
            if (r + dr, c + dc) == (from_r, from_c):
                continue
            arms.append((r + dr, c + dc, r, c, dist + 1))


if __name__ == '__main__':
    main()

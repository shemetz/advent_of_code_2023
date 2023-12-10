def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    # ADD PADDING - this is helpful for part 2's fill and to avoid boundary checks in part 1
    input_lines = ["#" + line + "#" for line in input_lines]
    input_lines = ["#" * len(input_lines[0])] + input_lines + ["#" * len(input_lines[0])]
    up, down, left, right, = -1, +1, -1j, +1j
    grid = {}
    start_coords = -1 - 1j
    for r, line in enumerate(input_lines):
        for c, char in enumerate(line):
            pos = r + c * 1j
            grid[pos] = char
            if char == 'S':
                start_coords = pos
    for start_direction in [up, down, left, right]:
        position = start_coords
        direction = start_direction
        visited = set()
        path_taken = []
        while position not in visited:
            visited.add(position)
            position += direction
            if grid[position] in 'S.#':
                break
            prev_direction = direction
            if grid[position] == '|' and direction in [up, down]:
                pass  # still the same direction
            elif grid[position] == '-' and direction in [left, right]:
                pass  # still the same direction
            elif any([
                grid[position] == 'L' and direction == down,
                grid[position] == 'J' and direction == right,
                grid[position] == '7' and direction == up,
                grid[position] == 'F' and direction == left,
            ]):
                direction = direction * +1j  # turn left
            elif any([
                grid[position] == 'L' and direction == left,
                grid[position] == 'J' and direction == down,
                grid[position] == '7' and direction == right,
                grid[position] == 'F' and direction == up,
            ]):
                direction = direction * -1j  # turn right
            else:
                position = None
                break
            path_taken.append((position, direction, prev_direction))
            # BIG ASSUMPTION:  loop goes counterclockwise (arbitrary)
        if position == start_coords:  # successful loop
            break
    print("Part 1:", len(visited) // 2)  # 6754

    # now "fill" from those spots
    for attempt in ["clockwise", "counterclockwise"]:
        marked_inside_loop = set()
        if attempt == "clockwise":
            for position, direction, prev_direction in path_taken:
                if direction == prev_direction:  # if kept moving forwards, mark our relative right
                    marked_inside_loop.add(position + direction * -1j)
                if direction == prev_direction * +1j:  # if turned left, mark our relative down and right
                    marked_inside_loop.add(position + direction * -1)
                    marked_inside_loop.add(position + direction * -1j)
                if direction == prev_direction * -1j:  # if turned right, mark nothing
                    pass
        elif attempt == "counterclockwise":
            for position, direction, prev_direction in path_taken:
                if direction == prev_direction:  # if kept moving forwards, mark our relative left
                    marked_inside_loop.add(position + direction * +1j)
                if direction == prev_direction * -1j:  # if turned right, mark our relative down and left
                    marked_inside_loop.add(position + direction * -1)
                    marked_inside_loop.add(position + direction * +1j)
                if direction == prev_direction * +1j:  # if turned left, mark nothing
                    pass
        marked_inside_loop.difference_update(visited)
        # greedy fill, it's fine because we'll break if we reach outer bounds
        filled = set()
        frontier = list(marked_inside_loop)
        while frontier:
            position = frontier.pop()
            if grid[position] == "#":
                # artificial boundary, `break` will prevent `else: break` and thus continue for another attempt
                break
            if position in filled:
                continue
            if position in visited:
                continue
            filled.add(position)
            for direction in [up, down, left, right]:
                new_position = position + direction
                frontier.append(new_position)
        else:  # did not break, i.e. did not reach outer bounds
            break
    print("Part 2:", len(filled))  # 567


if __name__ == '__main__':
    main()

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

UP, DOWN, LEFT, RIGHT = (0, 1), (0, -1), (-1, 0), (1, 0)
LETTER_TO_DIRECTION = {"U": UP, "D": DOWN, "L": LEFT, "R": RIGHT}
DIRECTIONS_IN_ORDER = "RDLU"
PLOT_POLYGON = False


def solve(part: int):
    spot = (0, 0)
    polygon = [spot]
    clockwise = True
    last_dir = None
    for line in input_lines:
        # e.g. U 2 (#7a21e3)
        if part == 1:
            direction, s_steps, _color = line.split(' ')
            steps = int(s_steps)
        else:
            _direction, _steps, s_color = line.split(' ')
            steps = int(s_color[2:-2], 16)
            direction = DIRECTIONS_IN_ORDER[int(s_color[-2])]
        x, y = spot
        dx, dy = LETTER_TO_DIRECTION[direction]
        if last_dir is not None:
            pdx, pdy = LETTER_TO_DIRECTION[last_dir]
            clockwise = (dx == pdy and dy == -pdx)  # neat little trick that I figured out
        if clockwise:
            steps += 1  # to account for the pixel being fuller than a normal polygon would be (because low res grid)
        else:  # undo one step
            # noinspection PyUnboundLocalVariable
            x, y = x - pdx, y - pdy
            polygon[-1] = (x, y)
        # move
        spot = (x + steps * dx, y + steps * dy)
        polygon.append(spot)
        last_dir = direction

    cumulative_sum = 0
    for i in range(len(polygon) - 1):
        x1, y1 = polygon[i]
        x2, y2 = polygon[i + 1]
        cumulative_sum += x1 * y2 - x2 * y1
    polygon_area = int(abs(cumulative_sum) / 2)
    print(polygon_area)

    if part == 1 and PLOT_POLYGON:
        # paint polygon (I'm using AI copilot here a little)
        min_x = min(x for x, y in polygon)
        min_y = min(y for x, y in polygon)
        max_x = max(x for x, y in polygon)
        max_y = max(y for x, y in polygon)
        plt.figure().add_subplot(111).add_patch(Polygon(polygon, closed=True, color="red"))
        plt.axis([min_x - 1, max_x + 1, min_y - 1, max_y + 1])
        plt.axis('equal')
        plt.axis('off')
        plt.show()


solve(1)  # 46359
solve(2)  # 59574883048274

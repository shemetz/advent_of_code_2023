import re
from collections import defaultdict
from typing import List, NamedTuple, Dict, Optional, Set

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

Point3D = NamedTuple("Point3D", x=int, y=int, z=int)
Brick = NamedTuple("Brick", start=Point3D, end=Point3D)

GROUND_LEVEL = 1

starting_bricks: List[Brick] = []
for line in input_lines:
    x1, y1, z1, x2, y2, z2 = map(int, re.split('[,~]', line))
    if z1 > z2:
        # flip, to ensure all bricks start at lower z and end at higher z
        z1, z2 = z2, z1
    starting_bricks.append(Brick(start=Point3D(x1, y1, z1), end=Point3D(x2, y2, z2)))

bricks_by_z = sorted(starting_bricks, key=lambda b: b.start.z)
space: Dict[Point3D, Optional[Brick]] = defaultdict(lambda: None)
rested_bricks: List[Brick] = []
lone_supports: Set[Brick] = set()
for brick in bricks_by_z:
    x1, y1, z1 = brick.start
    x2, y2, z2 = brick.end
    x_range = range(x1, x2 + 1)
    y_range = range(y1, y2 + 1)
    while z1 > GROUND_LEVEL and all(space[Point3D(x, y, z1 - 1)] is None for x in x_range for y in y_range):
        z1 -= 1
        z2 -= 1
    z_range = range(z1, z2 + 1)
    brick = Brick(start=Point3D(x1, y1, z1), end=Point3D(x2, y2, z2))
    rested_bricks.append(brick)
    if z1 != GROUND_LEVEL:
        # resting on at least one other brick
        supporting_bricks = set()
        for x in x_range:
            for y in y_range:
                b2 = space[Point3D(x, y, z1 - 1)]
                if b2 is not None:
                    supporting_bricks.add(b2)
        if len(supporting_bricks) == 1:
            lone_supports.add(supporting_bricks.pop())
    for x in x_range:
        for y in y_range:
            for z in z_range:
                space[Point3D(x, y, z)] = brick

print(len(rested_bricks) - len(lone_supports))  # 405

old_rested_bricks = rested_bricks.copy()
total_falls = 0
for lone_support in lone_supports:
    bricks_by_z = sorted(old_rested_bricks, key=lambda b: b.start.z)
    bricks_by_z.remove(lone_support)
    space: Dict[Point3D, Optional[Brick]] = defaultdict(lambda: None)
    rested_bricks: List[Brick] = []
    for brick in bricks_by_z:
        x1, y1, z1 = brick.start
        x2, y2, z2 = brick.end
        x_range = range(x1, x2 + 1)
        y_range = range(y1, y2 + 1)
        fell = False
        while z1 > GROUND_LEVEL and all(space[Point3D(x, y, z1 - 1)] is None for x in x_range for y in y_range):
            z1 -= 1
            z2 -= 1
            fell = True
        total_falls += int(fell)
        z_range = range(z1, z2 + 1)
        brick = Brick(start=Point3D(x1, y1, z1), end=Point3D(x2, y2, z2))
        rested_bricks.append(brick)
        for x in x_range:
            for y in y_range:
                for z in z_range:
                    space[Point3D(x, y, z)] = brick

print(total_falls)  # 61297

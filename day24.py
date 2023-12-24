import itertools
import re
import z3
from typing import NamedTuple, List

Hailstone = NamedTuple("Hailstone", px=int, py=int, pz=int, vx=int, vy=int, vz=int, slope=float, intercept=float)

# INPUT PARSING

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]
test_area = (7, 27) if len(input_lines) < 9 else (200000000000000, 400000000000000)
hailstones: List[Hailstone] = []
for line in input_lines:
    px, py, pz, vx, vy, vz = [int(s) for s in re.findall(r'-?\d+', line)]
    # create line equations
    # y = ax + b
    slope = vy / vx
    intercept = py - slope * px
    hailstones.append(Hailstone(px, py, pz, vx, vy, vz, slope, intercept))

# PART 1

counter = 0
for h1, h2 in itertools.combinations(hailstones, 2):
    h1: Hailstone
    h2: Hailstone
    # find intersection
    # ax + b = cx + d
    # ax - cx = d - b
    # x(a - c) = d - b
    # x = (d - b) / (a - c)
    if h1.slope == h2.slope:
        continue  # parallel
    ix = (h2.intercept - h1.intercept) / (h1.slope - h2.slope)
    iy = h1.slope * ix + h1.intercept
    # ignore if behind starting points
    t1 = (ix - h1.px) / h1.vx
    t2 = (ix - h2.px) / h2.vx
    if t1 < 0 or t2 < 0:
        continue
    if test_area[0] <= ix <= test_area[1] and test_area[0] <= iy <= test_area[1]:
        counter += 1
print(counter)  # 12938

# PART 2

# note - these are actually all ints in the solution, but typing them as reals makes Z3 work faster ¯\_(ツ)_/¯
pxr, pyr, pzr, vxr, vyr, vzr = z3.Reals("pxr pyr pzr vxr vyr vzr")
solver = z3.Solver()
# only 3 hailstones are needed here;  each creates 1 variable and 3 equations, for a total of 9 vars and 9 eqs
for k, h in enumerate(hailstones[:3]):
    tK = z3.Real(f"t{k}")
    solver.add(tK > 0)
    solver.add(pxr + tK * vxr == h.px + tK * h.vx)
    solver.add(pyr + tK * vyr == h.py + tK * h.vy)
    solver.add(pzr + tK * vzr == h.pz + tK * h.vz)
solver.check()
total = sum(solver.model()[var].as_long() for var in [pxr, pyr, pzr])
print(total)  # 976976197397181

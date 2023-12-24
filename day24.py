import itertools
from z3 import Int, Ints, Solver

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

test_area = (7, 27) if len(input_lines) < 9 else (200000000000000, 400000000000000)

counter = 0
hailstones = []
for line in input_lines:
    px, py, pz, vx, vy, vz = [int(s) for s in line.replace(",", "").replace("@ ", "").split(" ") if s]
    hailstones.append((px, py, pz, vx, vy, vz))

for h1, h2 in itertools.combinations(hailstones, 2):
    px1, py1, pz1, vx1, vy1, vz1 = h1
    px2, py2, pz2, vx2, vy2, vz2 = h2
    # create line equations
    # y = ax + b
    slope_1 = vy1 / vx1
    inter_1 = py1 - slope_1 * px1
    slope_2 = vy2 / vx2
    inter_2 = py2 - slope_2 * px2
    # find intersection
    # ax + b = cx + d
    # ax - cx = d - b
    # x(a - c) = d - b
    # x = (d - b) / (a - c)
    if slope_1 == slope_2:
        continue  # parallel
    ix = (inter_2 - inter_1) / (slope_1 - slope_2)
    iy = slope_1 * ix + inter_1
    # ignore if behind starting points
    t1 = (ix - px1) / vx1
    t2 = (ix - px2) / vx2
    if t1 < 0 or t2 < 0:
        continue
    if test_area[0] <= ix <= test_area[1] and test_area[0] <= iy <= test_area[1]:
        counter += 1

print(counter)  # 12938

pxr, pyr, pzr, vxr, vyr, vzr = Ints("pxr pyr pzr vxr vyr vzr")
s = Solver()
for k, h in enumerate(hailstones[:3]):
    tK = Int(f"t{k}")
    s.add(tK > 0)
    pxh, pyh, pzh, vxh, vyh, vzh = h
    s.add(pxr + tK * vxr == pxh + tK * vxh)
    s.add(pyr + tK * vyr == pyh + tK * vyh)
    s.add(pzr + tK * vzr == pzh + tK * vzh)
s.check()
pxr = s.model()[pxr].as_long()
pyr = s.model()[pyr].as_long()
pzr = s.model()[pzr].as_long()
print(pxr + pyr + pzr)  # 976976197397181

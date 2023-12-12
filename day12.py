from functools import lru_cache
from typing import Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]


@lru_cache()
def recursive_arrangements(pixels: str, groups: Tuple[int]):
    if all(c == "." for c in pixels):
        if len(groups) == 0:
            return 1
        else:
            return 0
    if pixels.startswith("."):
        return recursive_arrangements(pixels.strip("."), groups)
    if pixels.startswith("#"):
        if len(groups) == 0:
            return 0
        if len(pixels) < groups[0]:
            return 0
        if any(c == "." for c in pixels[0:groups[0]]):
            return 0
        if len(groups) > 1:
            if len(pixels) < groups[0] + 1 or pixels[groups[0]] == "#":
                return 0
            return recursive_arrangements(pixels[groups[0] + 1:], groups[1:])
        else:
            return recursive_arrangements(pixels[groups[0]:], groups[1:])
    if pixels.startswith("?"):
        return recursive_arrangements(pixels.replace("?", ".", 1), groups) \
            + recursive_arrangements(pixels.replace("?", "#", 1), groups)


for part in [1, 2]:
    total_arrangements = 0
    for line in input_lines:
        left, right_s = line.split(" ")
        right = tuple([int(x) for x in right_s.split(",")])
        if part == 2:
            left = "?".join([left] * 5)
            right = right * 5
        # left = pixels (as string), right = groups (as tuple of ints)
        total_arrangements += recursive_arrangements(left, right)
    print(total_arrangements)  # 7118, 7030194981795

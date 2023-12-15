from collections import defaultdict
from typing import Dict, List, Tuple

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

initialization_sequence = input_lines[0].split(',')


def h_a_s_h(s):
    currsum = 0
    for c in s:
        currsum = ((currsum + ord(c)) * 17) % 256
    return currsum


print(sum(h_a_s_h(s) for s in initialization_sequence))  # 502139

boxes: Dict[int, List[Tuple[str, int]]] = defaultdict(list)
for command in initialization_sequence:
    if command.endswith("-"):
        label = command[:-1]
        key = h_a_s_h(label)
        box = boxes[key]
        for i, (k, v) in enumerate(box):
            if k == label:
                box.pop(i)
                break
    else:
        label, value_s = command.split("=")
        key = h_a_s_h(label)
        value = int(value_s)
        box = boxes[key]
        for i, (k, v) in enumerate(box):
            if k == label:
                box[i] = (label, value)
                break
        else:
            box.append((label, value))

total_focusing_power = sum(
    sum(
        (1 + box_key) * (1 + i) * value
        for i, (key, value) in enumerate(box)
    )
    for box_key, box in boxes.items()
)
print(total_focusing_power)  # 284132

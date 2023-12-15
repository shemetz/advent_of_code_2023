sequence, boxes = open("input.txt").readline().split(','), [{} for _ in range(256)]
h_a_s_h = lambda s, to_i=-1: (((h_a_s_h(s, to_i - 1) + ord(s[to_i])) * 17) % 256) if to_i >= -len(s) else 0
print(sum(h_a_s_h(s) for s in sequence))  # Part 1: 502139
for command in sequence:
    match command.strip("-").split("="):
        case [label, value]:
            boxes[h_a_s_h(label)][label] = int(value)  # python dicts maintain order :)
        case [label]:
            boxes[h_a_s_h(label)].pop(label, None)
print(sum(bi * ki * v for bi, box in enumerate(boxes, 1) for ki, (_, v) in enumerate(box.items(), 1)))  # Part 2: 284132

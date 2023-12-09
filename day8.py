import re
from math import lcm


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]

    leftright = input_lines[0]
    lrn = len(leftright)
    node_neighbors = {}
    for line in input_lines[2:]:
        node, left, right = re.match(r'(\w+) = \((\w+), (\w+)\)', line).groups()
        node_neighbors[node] = (left, right)

    count = 0
    curr = "AAA"
    while curr != "ZZZ":
        left, right = node_neighbors[curr]
        if leftright[count % lrn] == "L":
            curr = left
        else:
            curr = right
        count += 1
    print(count)  # 21251

    # seen = set()
    # count = 0
    # currs = {n for n in node_neighbors if n.endswith("A")}
    # while not all(c.endswith("Z") for c in currs):
    #     seen.add(frozenset(currs))
    #     currs = {
    #         node_neighbors[c][0] if leftright[count % lrn] == "L" else node_neighbors[c][1]
    #         for c in currs
    #     }
    #     count += 1
    # print(count)

    # 1. for each node, create an array of which Z-nodes it reaches and when
    #
    # 3. something something lcm?  I don't know

    loop_lengths = []
    for node in node_neighbors:
        if not node.endswith("A"):
            continue
        seen = {}
        count = 0
        while (node, count % lrn) not in seen:
            seen[(node, count % lrn)] = count
            node = node_neighbors[node][0] if leftright[count % lrn] == "L" else node_neighbors[node][1]
            count += 1
        # loop completed
        loop_start = seen[(node, count % lrn)]
        loop_lengths.append(count - loop_start)
        # APPARENTLY (NO IDEA WHY!) the loop starts are always Z nodes!
        # for node, mod in seen:
        #     if seen[(node, mod)] >= loop_start and node.endswith("Z"):
        #         print(mod, node)
        # APPARENTLY (NO IDEA WHY!) I don't need to care about loop start, only loop length
    print(lcm(*loop_lengths))  # 11678319315857


if __name__ == '__main__':
    main()

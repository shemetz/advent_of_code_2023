import networkx as nx
from collections import defaultdict
from matplotlib import pyplot as plt

with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]

G = nx.Graph()
graph = defaultdict(set)
for line in input_lines:
    line = line.replace(":", "").split(' ')
    first, *more = line
    # if first in SKIPPED: continue
    graph[first] = set(more)
    for other in more:
        # if other in SKIPPED: continue
        graph[other].add(first)
        G.add_edge(first, other)

nx.draw_networkx(G)
plt.show()

# found manually by visualization:
G.remove_edge("xgs", "lmj")
G.remove_edge("hgk", "pgz")
G.remove_edge("qnz", "gzr")

nx.draw_networkx(G)
plt.show()

cclms = 1
for cc in nx.connected_components(G):
    cclms *= len(cc)
print("Answer:", cclms)  # 533628

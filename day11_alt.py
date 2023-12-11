"""
Solution created from someone else's solution:
https://topaz.github.io/paste/#XQAAAQBbAQAAAAAAAAAzHIoib6p4r/McpYgEEgWhHoa5LSRMkLbuJZj6LtAOjPl1QIpJiNwP/V0yu+PLk+ZRpFg0F9EeczhkZQVISv4/yWbBE8sAb353yKZwsbT9+pDzopcAQrvPpD51qwN69RdYgAWDFr3GfngK4dr4QnVVQ8X2cx5P9yFWeuq1FtKOC/pzqWDLwiAPMIWKhp3wTdfqc1lpld0N2jTiA7ecPNeFucOr0Vbx8Mp53eoALgJ6+zVOoMqeyPo3Y/ca0zD9LuqArc+rhgWcg1lFidkpZz1u1A0x9n7v4P3LgZV+EbhhN1iYVokIw08n+Zf0HG4afv1lWSulSpv+koPs

I just refactored and added a lot of comments
"""
from itertools import accumulate, combinations


def sum_distances_in_one_dimension(coords_1d, empty_gap_size):
    # coords_1d has galaxy coordinates in one dimension, e.g:
    # [1, 2, 5, 6, 7, 10, ...]
    # expanded_coords_1d are the same coordinates but with gaps expanded:
    # [1, 2, 2000003, 2000004, 2000005, 4000006, ...]
    *expanded_coords_1d, = accumulate(
        1 if coord_1d in coords_1d else empty_gap_size
        for coord_1d in range(max(coords_1d) + 1)
    )
    return sum(
        # distance between galaxies is "manhattan distance", i.e. absolute delta in each dimension, summed up later
        abs(expanded_coords_1d[a] - expanded_coords_1d[b])
        # sum for each pair of galaxies (across just one dimension)
        for a, b in combinations(coords_1d, 2)
    )


# a list of (x, y) tuples, only galaxies
# (x for row, y for column)
# e.g. [(1, 0), (2, 1), (5, 2), ...]
galaxies = [(x, y) for y, row in enumerate(open('input.txt')) for x, char in enumerate(row)
            if char == '#']
# two tuples, one for all Xs and one for all Ys
# e.g. [(1, 1, 5, ...), (0, 1, 2, ...)]
galaxy_1d_xs_and_ys = list(zip(*galaxies))

# Part 1 uses gap size of 2, and part 2 uses gap size of 1000000 (one million)
for gap_size in 2, 1_000_000:
    print(sum(
        # manhattan distance means we can calculate distances in each dimension separately and add them up
        sum_distances_in_one_dimension(galaxy_coords_1d, gap_size)
        for galaxy_coords_1d in galaxy_1d_xs_and_ys
    ))

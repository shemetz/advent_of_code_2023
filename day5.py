from itertools import takewhile


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    initial_seeds = [int(s) for s in input_lines[0].split(" ")[1:]]
    it_l = iter(input_lines[2:])
    # split by empty lines
    maps = [[e] + list(takewhile(lambda e: e.strip('\n') != "", it_l)) for e in it_l if e.strip() != "'\n'"]
    # remove "x-to-y map:"
    maps = [m[1:] for m in maps]
    # split and convert into ints
    maps = [[[int(s) for s in rangemap.split(" ")] for rangemap in phase] for phase in maps]

    lowest_loc = 99999999999
    for initial_seed in initial_seeds:
        seed = initial_seed
        #
        # print(seed, end=" ")
        for phase in maps:
            for rangemap in phase:
                dest_start, src_start, length = rangemap
                if src_start <= seed < src_start + length:
                    seed = dest_start + seed - src_start
                    break
            else:
                seed = seed  # yeah
            # print(seed, end=" ")
        if seed < lowest_loc:
            lowest_loc = seed
        # print(seed)
    print(lowest_loc)  # 196167384

    # now the initial seeds are actually ranges/intervals that come in pairs...
    initial_ranges = []
    for i in range(len(initial_seeds) // 2):
        range_start = initial_seeds[2 * i]
        range_len = initial_seeds[2 * i + 1]
        initial_ranges.append((range_start, range_start + range_len))

    current_intervals = set(initial_ranges.copy())
    for phase in maps:
        next_intervals = set()
        while current_intervals:
            interval = current_intervals.pop()
            int_start, int_end = interval  # note:  [5,6,7] has start=5 and end=8
            for rangemap in phase:
                dest_start, src_start, range_length = rangemap
                src_end = src_start + range_length
                if int_end <= src_start or src_end <= int_start:
                    # is____ie    ss    se
                    # ss    se    is____ie
                    # no intersection
                    continue
                delta = dest_start - src_start
                if int_start < src_start <= int_end:
                    # is____ss    ??    ie    ??
                    # break at ss, leave is-ss to other rangemaps
                    current_intervals.add((int_start, src_start))
                if int_start <= src_end < int_end:
                    # ??    is    ??    se____ie
                    # break at se, leave se-ie to other rangemaps
                    current_intervals.add((src_end, int_end))
                if src_start <= int_start < src_end <= int_end:
                    # ss    is^^^^se____ie
                    # map is-se, break at se (left se-ie already)
                    next_intervals.add((int_start + delta, src_end + delta))
                if int_start <= src_start < int_end <= src_end:
                    # is____ss^^^^ie    se
                    # map ss-ie, break at se (left is-ss already)
                    next_intervals.add((src_start + delta, int_end + delta))
                if src_start <= int_start < int_end <= src_end:
                    # ss    is^^^^ie    se
                    # map is-ie
                    next_intervals.add((int_start + delta, int_end + delta))
                if int_start <= src_start < src_end <= int_end:
                    # is____ss^^^^se____ie
                    # map ss-se
                    next_intervals.add((src_start + delta, src_end + delta))
                break
            else:
                next_intervals.add(interval)
        current_intervals = next_intervals
    print(min(interval[0] for interval in current_intervals))  # 125742456


if __name__ == '__main__':
    main()

from itertools import takewhile

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
            destination_start, source_start, length = rangemap
            if source_start <= seed < source_start + length:
                seed = destination_start + seed - source_start
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
        if interval[0] == interval[1]:
            # empty interval
            continue


        def split_up():
            int_start, int_end = interval  # note:  [5,6,7] has start=5 and end=8
            for rangemap in phase:
                dest_start, src_start, range_length = rangemap
                src_end = src_start + range_length
                delta = dest_start - src_start
                if src_start <= int_start < src_end <= int_end:
                    #         is__________ie
                    #           ****  vvvv
                    #   ss__________se
                    # map is-se, continue with se-ie
                    current_intervals.add((src_end, int_end))
                    return int_start + delta, src_end + delta
                if int_start <= src_start < int_end <= src_end:
                    #   is__________ie
                    #     vvvv  ****
                    #         ss__________se
                    # map ss-ie, continue with is-ss
                    current_intervals.add((int_start, src_start))
                    return src_start + delta, int_end + delta
                if src_start <= int_start < int_end <= src_end:
                    #         is____ie
                    #           ****
                    #   ss________________se
                    # map is-ie
                    return int_start + delta, int_end + delta
                if int_start <= src_start < src_end <= int_end:
                    #   is________________ie
                    #     vvvv  ****  vvvv
                    #         ss____se
                    # map ss-se, continue with is-ss and with se-ie
                    current_intervals.add((int_start, src_start))
                    current_intervals.add((src_end, int_end))
                    return src_start + delta, src_end + delta
                # else, int_end <= src_start
                #   is____ie    ss    se
                # or src_end <= int_start:
                #   ss    se    is____ie
                # either way, no intersection with this range, but we keep going to test other ranges
            return None  # did not intersect with any range


        split_up_piece = split_up()
        if split_up_piece:
            next_intervals.add(split_up_piece)
        else:  # if did not intersect with any range, it just maps to itself
            next_intervals.add(interval)
    current_intervals = next_intervals
print(min(interval[0] for interval in current_intervals))  # 125742456

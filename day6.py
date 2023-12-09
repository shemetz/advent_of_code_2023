import re


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]

    def run_and_solve():
        times = [int(s) for s in re.findall(r"\d+", input_lines[0])]
        record_distances = [int(s) for s in re.findall(r"\d+", input_lines[1])]
        race_count = len(times)
        num_of_ways_to_win = 1
        for ri in range(race_count):
            time = times[ri]
            record_distance = record_distances[ri]
            ways_to_win_this_race = 0
            for t_pressed in range(1, time):
                speed = t_pressed
                t_remaining = time - t_pressed
                distance_traveled = speed * t_remaining
                if distance_traveled > record_distance:
                    ways_to_win_this_race += 1
            num_of_ways_to_win *= ways_to_win_this_race
        return num_of_ways_to_win

    print(run_and_solve())  # 2612736

    # for part 2, I just... removed spaces in input and ran it again and it worked in like 5 seconds :D
    # but here it is in code form:
    input_lines = [line.replace(" ", "").replace(":", ":    ") for line in input_lines]
    print(run_and_solve())  # 29891250


if __name__ == '__main__':
    main()

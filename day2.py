def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]

    limits = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    def is_possible(draw_strings):
        for ds in draw_strings:
            # example: 3 blue, 4 red
            partial_draws = ds.split(",")
            for pd in partial_draws:
                # example: 3 blue
                draw_num_s, color = pd.strip().split(" ")
                draw_num = int(draw_num_s)
                if draw_num > limits[color]:
                    return False
        return True

    def set_needed(draw_strings):
        needed = {
            "red": 0,
            "green": 0,
            "blue": 0,
        }
        for ds in draw_strings:
            # example: 3 blue, 4 red
            partial_draws = ds.split(",")
            for pd in partial_draws:
                # example: 3 blue
                draw_num_s, color = pd.strip().split(" ")
                draw_num = int(draw_num_s)
                needed[color] = max(needed[color], draw_num)
        return needed

    sum_ids = 0
    sum_powers = 0
    for line in input_lines:
        # example: Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        game_num_s, draws_line = line.split(":")
        game_num = int(game_num_s.split(" ")[1])
        draw_strings = draws_line.split(";")
        if is_possible(draw_strings):
            sum_ids += game_num
        needed = set_needed(draw_strings)
        sum_powers += needed["red"] * needed["green"] * needed["blue"]
    print(sum_ids)  # 2545
    print(sum_powers)  # 78111


if __name__ == '__main__':
    main()

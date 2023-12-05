import re
from collections import defaultdict


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    # example line:
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    score_sum = 0
    for line in input_lines:
        winners_s, mine_s = line.split(":")[1].split("|")
        winners = [int(s) for s in winners_s.strip().split(" ") if s.strip()]
        mine = [int(s) for s in mine_s.strip().split(" ") if s.strip()]
        score = 0
        for num in mine:
            if num in winners:
                if score == 0:
                    score = 1
                else:
                    score = score * 2
        score_sum += score
    print(score_sum)  # 26426

    boards_count = 0
    memo = defaultdict(lambda: 0)
    n = len(input_lines)  # with 6 cards, n = 6
    for i in range(n):
        k = n - i - 1  # counting down from n to 1
        line = input_lines[k]
        winners_s, mine_s = line.split(":")[1].split("|")
        winners = [int(s) for s in winners_s.strip().split(" ") if s.strip()]
        mine = [int(s) for s in mine_s.strip().split(" ") if s.strip()]
        win_count = sum([1 for num in mine if num in winners])
        memo[k] = 1 + sum(memo[k] for k in range(k + 1, k + 1 + win_count))
        boards_count += memo[k]
    print(boards_count)  # 6227972


if __name__ == '__main__':
    main()

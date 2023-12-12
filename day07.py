with open("input.txt") as input_file:
    input_lines = input_file.readlines()
    input_lines = [line.strip('\n') for line in input_lines]
strengths_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]
score_by_card_counts = {1: 0, 2: 1, 3: 3, 4: 5, 5: 6}

players = []
for line in input_lines:
    hand_s, bid_s = line.split(" ")
    players.append((hand_s, int(bid_s)))


def calc_type_score(hand: str):
    return sum(score_by_card_counts[hand.count(letter)] for letter in set(hand))


def make_sorting_key(hand_score, hand_letters):
    return -hand_score, *[strengths_order.index(letter) for letter in hand_letters]


def calc_sorting_key(hand: str):
    hand_type_score = calc_type_score(hand)
    return make_sorting_key(hand_type_score, hand)


def calc_sum_winnings(sorted_unranked_players):
    ranked_players = [(rank + 1, player) for rank, player in enumerate(sorted_unranked_players)]
    winnings = [rank * bid for rank, (_hand, bid) in ranked_players]
    return sum(winnings)


sorted_players = sorted(players, key=lambda x: calc_sorting_key(x[0]), reverse=True)
print(calc_sum_winnings(sorted_players))  # 250946742

strengths_order.remove("J")
strengths_order.append("J")


def calc_sorting_key_with_j(hand: str):
    most_frequent_non_j = max(set(hand.replace("J", "")), key=hand.count) if hand != "JJJJJ" else "2"
    hand_type_score = calc_type_score(hand.replace("J", most_frequent_non_j))
    return make_sorting_key(hand_type_score, hand)


sorted_players = sorted(players, key=lambda x: calc_sorting_key_with_j(x[0]), reverse=True)
print(calc_sum_winnings(sorted_players))  # 251824095

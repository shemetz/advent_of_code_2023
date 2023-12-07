import re


def main():
    with open("input.txt") as input_file:
        input_lines = input_file.readlines()
        input_lines = [line.strip('\n') for line in input_lines]
    strengths_order = ["A", "K", "Q", "J", "T", "9", "8", "7", "6", "5", "4", "3", "2"]

    players = []
    for line in input_lines:
        hand_s, bid_s = line.split(" ")
        players.append((hand_s, int(bid_s)))

    def calc_type(hand: str):
        if hand == hand[0] * 5:
            return 1, "five of a kind"
        if len(set(hand)) == 2:
            if hand.count(hand[0]) == 4 or hand.count(hand[1]) == 4:
                return 2, "four of a kind"
            return 3, "full house"
        if len(set(hand)) == 3:
            for card in hand:
                if hand.count(card) == 3:
                    return 4, "three of a kind"
        if len(set(hand)) == 3 and (
                hand.count(hand[0]) == 2
                or hand.count(hand[1]) == 2
        ):
            return 5, "two pairs"
        if len(set(hand)) == 4:
            return 6, "one pair"
        return 7, "high card"

    def calc_sorting_key(hand: str):
        best_type_num, best_type_name = calc_type(hand)
        letters_as_numbers = [strengths_order.index(letter) for letter in hand]
        # print(hand, best_type_name, *letters_as_numbers)
        return best_type_num, *letters_as_numbers

    sorted_players = sorted(players, key=lambda x: calc_sorting_key(x[0]), reverse=True)
    ranked_players = [(rank + 1, player) for rank, player in enumerate(sorted_players)]
    winnings = [rank * bid for rank, (_hand, bid) in ranked_players]
    total_winnings = sum(winnings)
    print(total_winnings)  # 250946742

    strengths_order.remove("J")
    strengths_order.append("J")

    def calc_sorting_key_with_j(hand: str):
        most_frequent = max(set(hand.replace("J", "")), key=hand.count) if hand != "JJJJJ" else "2"
        best_type_num, best_type_name = calc_type(hand.replace("J", most_frequent))
        letters_as_numbers = [strengths_order.index(letter) for letter in hand]
        # print(hand, best_type_name, *letters_as_numbers)
        return best_type_num, *letters_as_numbers

    sorted_players = sorted(players, key=lambda x: calc_sorting_key_with_j(x[0]), reverse=True)
    ranked_players = [(rank + 1, player) for rank, player in enumerate(sorted_players)]
    winnings = [rank * bid for rank, (_hand, bid) in ranked_players]
    total_winnings = sum(winnings)
    print(total_winnings)  # 251824095


if __name__ == '__main__':
    main()

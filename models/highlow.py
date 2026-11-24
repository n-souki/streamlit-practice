import random


def draw_cards():
    suits = ("spades", "hearts", "diamonds", "clubs")
    deck = [
        {"suit": suit, "rank": rank}
        for suit in suits
        for rank in range(1, 14)
    ]
    return random.sample(deck, 2)


def win_probability(base_rank, choice):
    """Return the probability of winning against a fresh card."""
    winning_cards = (
        13 - base_rank if choice == "High" else base_rank - 1
    )
    return winning_cards / 13


def calculate_payout(points, bet, result):
    """Return the point change for a round."""
    if result == "win":
        return bet
    if result == "lose":
        return -bet
    return 0


def judge(base_rank, result_rank, choice):
    # 同じ数字なら引き分け
    if base_rank == result_rank:
        return "draw"

    # Highを選んだ場合
    if choice == "High":
        if result_rank > base_rank:
            return "win"
        else:
            return "lose"

    # Lowを選んだ場合
    if choice == "Low":
        if result_rank < base_rank:
            return "win"
        else:
            return "lose"

    return "invalid"
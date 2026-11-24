import unittest

from models.highlow import calculate_payout, judge, win_probability


class HighLowTests(unittest.TestCase):
    def test_existing_judge_behavior_is_preserved(self):
        self.assertEqual(judge(5, 9, "High"), "win")
        self.assertEqual(judge(5, 2, "High"), "lose")
        self.assertEqual(judge(5, 5, "Low"), "draw")

    def test_probability_uses_high_and_low_winning_cards(self):
        self.assertAlmostEqual(win_probability(5, "High"), 8 / 13)
        self.assertAlmostEqual(win_probability(5, "Low"), 4 / 13)

    def test_payout_is_bet_on_win_and_loss(self):
        self.assertEqual(calculate_payout(1000, 100, "win"), 100)
        self.assertEqual(calculate_payout(1000, 100, "lose"), -100)
        self.assertEqual(calculate_payout(1000, 100, "draw"), 0)


if __name__ == "__main__":
    unittest.main()

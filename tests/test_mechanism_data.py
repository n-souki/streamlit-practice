import unittest

from games.mechanism_data import (
    ELECTRON_CHALLENGES,
    PDH_STEPS,
    RESEARCH_CHALLENGES,
)


class MechanismDataTests(unittest.TestCase):
    def test_pdh_steps_have_unique_keys(self):
        keys = [step.key for step in PDH_STEPS]
        self.assertEqual(len(keys), len(set(keys)))

    def test_pdh_order_starts_with_tpp_ylide_and_ends_with_nadh(self):
        self.assertEqual(PDH_STEPS[0].key, "tpp_ylide")
        self.assertEqual(PDH_STEPS[-1].key, "nad_reoxidation")

    def test_pdh_includes_co2_and_coa_events(self):
        text = " ".join(step.description for step in PDH_STEPS)
        self.assertIn("CO2", text)
        self.assertIn("CoA", text)

    def test_choice_questions_have_valid_answers_and_explanations(self):
        for question in ELECTRON_CHALLENGES + RESEARCH_CHALLENGES:
            self.assertIn(question["difficulty"], {"基礎", "標準", "応用", "発展"})
            self.assertGreaterEqual(question["answer"], 0)
            self.assertLess(question["answer"], len(question["choices"]))
            self.assertTrue(question["explanation"])


if __name__ == "__main__":
    unittest.main()

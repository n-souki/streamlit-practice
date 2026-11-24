import unittest

from games.redox_engine import PATHWAYS, Resources, apply_pathway, ratio


class RedoxEngineTests(unittest.TestCase):
    def test_glycolysis_has_consistent_material_balance(self):
        initial = Resources(nad=2, adp=2, glucose=1)
        result = apply_pathway(initial, "glycolysis")

        self.assertEqual(result.glucose, 0)
        self.assertEqual(result.nad, 0)
        self.assertEqual(result.nadh, 2)
        self.assertEqual(result.adp, 0)
        self.assertEqual(result.atp, 2)
        self.assertEqual(result.pyruvate, 2)

    def test_electron_transport_requires_oxygen_and_nadh(self):
        initial = Resources(nadh=2, nad=0, adp=3, oxygen=1)
        result = apply_pathway(initial, "etc")

        self.assertEqual(result.nadh, 0)
        self.assertEqual(result.nad, 2)
        self.assertEqual(result.oxygen, 0)
        self.assertEqual(result.adp, 0)
        self.assertEqual(result.atp, 3)

    def test_pathway_rejects_insufficient_resources(self):
        with self.assertRaises(ValueError):
            apply_pathway(Resources(glucose=1, nad=1, adp=2), "glycolysis")

    def test_nadh_and_nadph_are_not_interchangeable(self):
        self.assertEqual(PATHWAYS["glycolysis"].changes["nadh"], 2)
        self.assertEqual(PATHWAYS["ppp"].changes["nadph"], 2)
        self.assertEqual(ratio(2, 4), 0.5)


if __name__ == "__main__":
    unittest.main()

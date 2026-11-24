import unittest

from games.survival_engine import (
    CellResources,
    PATHWAYS,
    finish_turn,
    health,
    run_pathway,
)


class SurvivalEngineTests(unittest.TestCase):
    def test_glycolysis_produces_atp_and_nadh_without_oxygen(self):
        result = run_pathway(
            CellResources(glucose=1, nad=2, adp=2),
            "glycolysis",
        )
        self.assertEqual(result.atp, 2)
        self.assertEqual(result.nadh, 2)
        self.assertEqual(result.oxygen, 0)

    def test_fermentation_regenerates_nad(self):
        result = run_pathway(
            CellResources(pyruvate=1, nadh=1),
            "fermentation",
        )
        self.assertEqual(result.nad, 1)
        self.assertEqual(result.nadh, 0)
        self.assertEqual(result.lactate, 1)

    def test_tca_produces_reducing_equivalents(self):
        result = run_pathway(
            CellResources(acetyl_coa=1, nad=3, fad=1, adp=1),
            "tca",
        )
        self.assertEqual(result.nadh, 3)
        self.assertEqual(result.fadh2, 1)
        self.assertEqual(result.atp, 1)

    def test_etc_requires_oxygen_and_makes_atp(self):
        result = run_pathway(
            CellResources(nadh=2, nad=0, adp=3, oxygen=1),
            "etc",
        )
        self.assertEqual(result.atp, 3)
        self.assertEqual(result.nad, 2)
        self.assertEqual(result.oxygen, 0)

    def test_turn_end_consumes_atp_and_supplies_nutrients(self):
        result = finish_turn(CellResources(atp=2, glucose=1, oxygen=0))
        self.assertEqual(result.atp, 1)
        self.assertEqual(result.glucose, 2)
        self.assertEqual(result.oxygen, 1)

    def test_pathway_definitions_keep_phase_one_scope(self):
        self.assertEqual(
            set(PATHWAYS),
            {"glycolysis", "fermentation", "tca", "etc"},
        )
        self.assertEqual(health(CellResources(atp=0))[0], "要注意")


if __name__ == "__main__":
    unittest.main()

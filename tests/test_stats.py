from __future__ import annotations

import unittest

from app.tools.experiment_stats import check_srm, compute_metric_lift


class ExperimentStatsTests(unittest.TestCase):
    def test_srm_fails_for_large_imbalance(self) -> None:
        rows = [{"group": "control"}, {"group": "control"}] + [{"group": "treatment"} for _ in range(18)]
        result = check_srm(rows)
        self.assertEqual(result["classification"], "fail")

    def test_metric_lift(self) -> None:
        rows = [
            {"group": "control", "revenue": "10"},
            {"group": "control", "revenue": "20"},
            {"group": "treatment", "revenue": "15"},
            {"group": "treatment", "revenue": "25"},
        ]
        result = compute_metric_lift(rows, "revenue")
        self.assertEqual(result["control_mean"], 15)
        self.assertEqual(result["treatment_mean"], 20)
        self.assertAlmostEqual(result["lift_pct"], 33.3333, places=3)


if __name__ == "__main__":
    unittest.main()


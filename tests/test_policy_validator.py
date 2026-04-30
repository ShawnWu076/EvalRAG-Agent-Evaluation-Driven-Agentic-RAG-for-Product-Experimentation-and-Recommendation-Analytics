from __future__ import annotations

import unittest

from app.policy_validator import validate_decision


class PolicyValidatorTests(unittest.TestCase):
    def test_srm_failure_overrides_launch(self) -> None:
        result = validate_decision(
            "The experiment has sample ratio mismatch but revenue looks higher.",
            "launch",
        )
        self.assertEqual(result["policy_decision"], "do_not_trust_result")
        self.assertEqual(result["final_decision"], "do_not_trust_result")
        self.assertTrue(result["policy_override"])

    def test_non_random_rollout_requires_quasi_experiment(self) -> None:
        result = validate_decision(
            "The feature was launched in one city with no randomized control and pre/post data.",
            "launch",
        )
        self.assertEqual(result["final_decision"], "use_did_or_quasi_experiment")

    def test_guardrail_regression_confirms_investigation(self) -> None:
        result = validate_decision(
            "Revenue increased but 7-day retention dropped.",
            "investigate_further",
        )
        self.assertEqual(result["policy_action"], "confirm")
        self.assertEqual(result["final_decision"], "investigate_further")

    def test_clean_win_supports_launch(self) -> None:
        result = validate_decision(
            "Revenue is significantly up, retention is stable, complaints are stable, and SRM passed.",
            "investigate_further",
        )
        self.assertTrue(result["policy_triggered"])
        self.assertEqual(result["policy_action"], "override")
        self.assertEqual(result["final_decision"], "launch")

    def test_ads_quality_drop_requires_investigation(self) -> None:
        result = validate_decision(
            "An ads experiment increased CTR but lowered advertiser conversion quality and ROAS.",
            "do_not_launch",
        )
        self.assertEqual(result["policy_decision"], "investigate_further")
        self.assertEqual(result["final_decision"], "investigate_further")

    def test_confidence_interval_downside_requires_investigation(self) -> None:
        result = validate_decision(
            "The primary metric improved, but the confidence interval includes meaningful downside on retention.",
            "launch",
        )
        self.assertEqual(result["policy_decision"], "investigate_further")


if __name__ == "__main__":
    unittest.main()

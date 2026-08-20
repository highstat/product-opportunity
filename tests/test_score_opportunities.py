from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.score_opportunities import ValidationError, score_payload  # noqa: E402


def score(score, confidence, evidence_id):
    return {"score": score, "confidence": confidence, "evidence_ids": [evidence_id]}


def opportunity(identifier, problem, reach, problem_evidence, reach_evidence, gate="pass"):
    return {
        "id": identifier,
        "name": identifier.upper(),
        "scores": {
            "problem": score(problem, 0.8, problem_evidence),
            "reachability": score(reach, 0.7, reach_evidence),
        },
        "fatal_gates": {
            "first_customer_path": {
                "status": gate,
                "evidence_ids": [] if gate == "unknown" else [reach_evidence],
                "reason": "explicit assessment",
            }
        },
    }


def valid_payload():
    return {
        "evidence": [{"id": "E1"}, {"id": "E2"}, {"id": "E3"}, {"id": "E4"}],
        "weights": {"problem": 50, "reachability": 50},
        "opportunities": [
            opportunity("alpha", 4, 4, "E1", "E2"),
            opportunity("beta", 3, 3, "E3", "E4"),
        ],
        "sensitivity_scenarios": [
            {"name": "problem-heavy", "weights": {"problem": 80, "reachability": 20}}
        ],
    }


class ScoreOpportunitiesTests(unittest.TestCase):
    def test_robust_winner(self):
        result = score_payload(valid_payload())
        self.assertEqual("robust", result["ranking"]["status"])
        self.assertEqual("alpha", result["ranking"]["winner_id"])
        self.assertEqual(["alpha", "beta"], result["ranking"]["base_order"])

    def test_deterministic_json_across_input_order(self):
        first = valid_payload()
        second = copy.deepcopy(first)
        second["opportunities"].reverse()
        second["evidence"].reverse()
        rendered_first = json.dumps(score_payload(first), sort_keys=True)
        rendered_second = json.dumps(score_payload(second), sort_keys=True)
        self.assertEqual(rendered_first, rendered_second)

    def test_weight_sum_must_be_100(self):
        payload = valid_payload()
        payload["weights"] = {"problem": 40, "reachability": 40}
        with self.assertRaisesRegex(ValidationError, "sum to 100"):
            score_payload(payload)

    def test_score_and_confidence_ranges_are_validated(self):
        payload = valid_payload()
        payload["opportunities"][0]["scores"]["problem"]["score"] = [3, 5]
        with self.assertRaisesRegex(ValidationError, "between 0 and 4"):
            score_payload(payload)
        payload = valid_payload()
        payload["opportunities"][0]["scores"]["problem"]["confidence"] = 1.1
        with self.assertRaisesRegex(ValidationError, "between 0 and 1"):
            score_payload(payload)

    def test_unknown_evidence_reference_is_rejected(self):
        payload = valid_payload()
        payload["opportunities"][0]["scores"]["problem"]["evidence_ids"] = ["MISSING"]
        with self.assertRaisesRegex(ValidationError, "unknown evidence ID"):
            score_payload(payload)

    def test_unknown_fatal_gate_makes_ranking_insufficient(self):
        payload = valid_payload()
        payload["opportunities"][0]["fatal_gates"]["first_customer_path"] = {
            "status": "unknown",
            "evidence_ids": [],
        }
        result = score_payload(payload)
        self.assertEqual("insufficient", result["ranking"]["status"])
        alpha = next(item for item in result["opportunities"] if item["id"] == "alpha")
        self.assertFalse(alpha["eligible"])
        self.assertEqual(["first_customer_path"], alpha["unknown_gates"])
        self.assertIsNone(alpha["scores"]["base"])

    def test_equal_base_scores_are_tied(self):
        payload = valid_payload()
        payload["opportunities"][1]["scores"] = copy.deepcopy(payload["opportunities"][0]["scores"])
        result = score_payload(payload)
        self.assertEqual("tied", result["ranking"]["status"])
        self.assertIsNone(result["ranking"]["winner_id"])

    def test_sensitivity_winner_change_is_fragile(self):
        payload = valid_payload()
        payload["opportunities"] = [
            opportunity("alpha", 4, 1, "E1", "E2"),
            opportunity("beta", 1, 4, "E3", "E4"),
        ]
        payload["weights"] = {"problem": 70, "reachability": 30}
        payload["sensitivity_scenarios"] = [
            {"name": "reachability-heavy", "weights": {"problem": 20, "reachability": 80}}
        ]
        result = score_payload(payload)
        self.assertEqual("fragile", result["ranking"]["status"])
        self.assertEqual("alpha", result["ranking"]["winner_id"])
        self.assertEqual("beta", result["ranking"]["scenario_winners"]["reachability-heavy"])

    def test_overlapping_score_ranges_are_fragile(self):
        payload = valid_payload()
        payload["opportunities"][0]["scores"]["problem"]["score"] = [2, 4]
        payload["opportunities"][0]["scores"]["reachability"]["score"] = [2, 4]
        payload["opportunities"][1]["scores"]["problem"]["score"] = [1.5, 3]
        payload["opportunities"][1]["scores"]["reachability"]["score"] = [1.5, 3]
        result = score_payload(payload)
        self.assertEqual("fragile", result["ranking"]["status"])

    def test_sensitivity_range_overlap_is_fragile_even_when_midpoint_winner_is_stable(self):
        payload = valid_payload()
        payload["opportunities"][0]["scores"]["problem"]["score"] = [3, 4]
        payload["opportunities"][0]["scores"]["reachability"]["score"] = 4
        payload["opportunities"][1]["scores"]["problem"]["score"] = [2, 4]
        payload["opportunities"][1]["scores"]["reachability"]["score"] = 2
        payload["weights"] = {"problem": 20, "reachability": 80}
        payload["sensitivity_scenarios"] = [
            {"name": "problem-heavy", "weights": {"problem": 90, "reachability": 10}}
        ]
        result = score_payload(payload)
        self.assertEqual("fragile", result["ranking"]["status"])
        self.assertTrue(result["ranking"]["scenario_range_overlaps"]["problem-heavy"])

    def test_explicit_minimum_confidence_can_make_rank_insufficient(self):
        payload = valid_payload()
        payload["minimum_confidence"] = 0.9
        result = score_payload(payload)
        self.assertEqual("insufficient", result["ranking"]["status"])
        self.assertIsNone(result["ranking"]["winner_id"])


if __name__ == "__main__":
    unittest.main()

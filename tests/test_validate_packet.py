from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.validate_packet import validate_packet  # noqa: E402


def valid_packet():
    return {
        "as_of": "2026-08-20",
        "evidence": [
            {
                "id": "E1",
                "url": "https://example.com/pricing",
                "origin_id": "example.com",
                "published_or_updated": "2026-08-01",
                "retrieved": "2026-08-20",
                "evidence_type": "price",
            },
            {
                "id": "E2",
                "url": "https://community.example.net/thread/1",
                "origin_id": "author-42",
                "published_or_updated": "2026-07-10",
                "retrieved": "2026-08-20",
                "evidence_type": "review",
            },
        ],
        "claims": [
            {
                "id": "C1",
                "status": "Fact",
                "topic": "price",
                "statement": "The current listed price is documented.",
                "evidence_ids": ["E1"],
            },
            {
                "id": "C2",
                "status": "Inference",
                "topic": "other",
                "statement": "The workflow may be costly.",
                "evidence_ids": ["E2"],
            },
        ],
        "opportunities": [
            {
                "id": "alpha",
                "first_customer_route": {
                    "status": "Evidenced",
                    "summary": "Buyer reaches the current offer through a permitted surface.",
                    "evidence_ids": ["E2"],
                },
                "scores": {
                    "problem": {"score": 4, "confidence": 0.7, "evidence_ids": ["E2"]}
                },
                "fatal_gates": {
                    "first_customer_path": {"status": "pass", "evidence_ids": ["E2"]},
                    "legal": {"status": "pass", "evidence_ids": ["E1"]},
                },
            }
        ],
        "build_boundary": {"status": "Open for specified scope", "reason": "all fatal gates pass"},
        "independence_claims": [
            {
                "evidence_ids": ["E1", "E2"],
                "independent": True,
                "basis": "Different original publishers and authors.",
            }
        ],
        "experiments": [
            {
                "id": "X1",
                "hypothesis": "A defined audience will make a costly commitment.",
                "success": "At least one paid pilot by the deadline.",
                "failure": "No paid pilot after completing the planned outreach.",
                "inconclusive": "The channel fails before enough prospects see the offer.",
            }
        ],
    }


def codes(result):
    return {error["code"] for error in result["errors"]}


class ValidatePacketTests(unittest.TestCase):
    def test_valid_packet(self):
        result = validate_packet(valid_packet())
        self.assertTrue(result["valid"], result["errors"])

    def test_fact_requires_evidence_and_url(self):
        packet = valid_packet()
        packet["claims"][0]["evidence_ids"] = []
        result = validate_packet(packet)
        self.assertIn("fact-evidence", codes(result))

        packet = valid_packet()
        packet["evidence"][0]["url"] = "not-a-url"
        result = validate_packet(packet)
        self.assertIn("fact-url", codes(result))

    def test_current_price_policy_and_competitor_facts_need_dates(self):
        for topic in ("price", "policy", "competitor"):
            with self.subTest(topic=topic):
                packet = valid_packet()
                packet["claims"][0]["topic"] = topic
                packet["evidence"][0]["evidence_type"] = topic
                packet["evidence"][0].pop("published_or_updated")
                result = validate_packet(packet)
                self.assertIn("current-date", codes(result))

    def test_score_requires_known_evidence_ids(self):
        packet = valid_packet()
        packet["opportunities"][0]["scores"]["problem"]["evidence_ids"] = []
        result = validate_packet(packet)
        self.assertIn("score-evidence", codes(result))

        packet = valid_packet()
        packet["opportunities"][0]["scores"]["problem"]["evidence_ids"] = ["MISSING"]
        result = validate_packet(packet)
        self.assertIn("evidence-ref", codes(result))

    def test_same_origin_cannot_be_claimed_independent(self):
        packet = valid_packet()
        packet["evidence"][1]["origin_id"] = "example.com"
        result = validate_packet(packet)
        self.assertIn("same-origin", codes(result))

    def test_route_status_must_match_first_customer_gate(self):
        packet = valid_packet()
        packet["opportunities"][0]["first_customer_route"]["status"] = "Conditional"
        result = validate_packet(packet)
        self.assertIn("route-gate", codes(result))

        packet["opportunities"][0]["fatal_gates"]["first_customer_path"]["status"] = "unknown"
        packet["opportunities"][0]["fatal_gates"]["first_customer_path"]["evidence_ids"] = []
        packet["build_boundary"]["status"] = "Closed"
        result = validate_packet(packet)
        self.assertTrue(result["valid"], result["errors"])

    def test_evidenced_route_requires_evidence(self):
        packet = valid_packet()
        packet["opportunities"][0]["first_customer_route"]["evidence_ids"] = []
        result = validate_packet(packet)
        self.assertIn("route-evidence", codes(result))

    def test_positive_independence_claim_needs_basis(self):
        packet = valid_packet()
        packet["independence_claims"][0]["basis"] = ""
        result = validate_packet(packet)
        self.assertIn("independence-basis", codes(result))

    def test_unknown_fatal_gate_requires_closed_build_boundary(self):
        packet = valid_packet()
        packet["opportunities"][0]["fatal_gates"]["legal"]["status"] = "unknown"
        packet["opportunities"][0]["fatal_gates"]["legal"]["evidence_ids"] = []
        result = validate_packet(packet)
        self.assertIn("build-boundary", codes(result))

        packet["build_boundary"]["status"] = "Closed"
        result = validate_packet(packet)
        self.assertTrue(result["valid"], result["errors"])

    def test_failed_fatal_gate_also_requires_closed_boundary(self):
        packet = valid_packet()
        packet["opportunities"][0]["fatal_gates"]["legal"]["status"] = "fail"
        result = validate_packet(packet)
        self.assertIn("build-boundary", codes(result))

    def test_resolved_fatal_gate_requires_known_evidence(self):
        packet = valid_packet()
        packet["opportunities"][0]["fatal_gates"]["legal"]["evidence_ids"] = []
        result = validate_packet(packet)
        self.assertIn("gate-evidence", codes(result))

        packet = valid_packet()
        packet["opportunities"][0]["fatal_gates"]["legal"]["evidence_ids"] = ["MISSING"]
        result = validate_packet(packet)
        self.assertIn("evidence-ref", codes(result))

    def test_experiment_requires_pass_fail_and_inconclusive_criteria(self):
        for field in ("success", "failure", "inconclusive"):
            with self.subTest(field=field):
                packet = valid_packet()
                packet["experiments"][0][field] = ""
                result = validate_packet(packet)
                self.assertIn("experiment-outcome", codes(result))

    def test_errors_are_deterministic(self):
        packet = valid_packet()
        packet["claims"][0]["evidence_ids"] = []
        packet["experiments"][0]["success"] = ""
        first = json.dumps(validate_packet(packet), sort_keys=True)
        second = json.dumps(validate_packet(copy.deepcopy(packet)), sort_keys=True)
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()

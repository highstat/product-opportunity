#!/usr/bin/env python3
"""Validate and score explicit product-opportunity assessments.

This module performs arithmetic and structural validation only. It never assigns
semantic scores, invents weights, researches a market, or makes a build decision.
"""

from __future__ import annotations

import argparse
from decimal import Decimal, InvalidOperation
import json
import sys
from typing import Any


SCORE_MIN = Decimal("0")
SCORE_MAX = Decimal("4")
CONFIDENCE_MIN = Decimal("0")
CONFIDENCE_MAX = Decimal("1")
WEIGHT_TOTAL = Decimal("100")
GATE_STATUSES = {"pass", "fail", "unknown"}


class ValidationError(ValueError):
    """Raised when scoring input violates the documented contract."""


def _decimal(value: Any, path: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, str, Decimal)):
        raise ValidationError(f"{path} must be a number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValidationError(f"{path} must be a finite number") from exc
    if not result.is_finite():
        raise ValidationError(f"{path} must be a finite number")
    return result


def _bounded(value: Any, path: str, minimum: Decimal, maximum: Decimal) -> Decimal:
    result = _decimal(value, path)
    if result < minimum or result > maximum:
        raise ValidationError(f"{path} must be between {minimum} and {maximum}")
    return result


def _range(
    value: Any,
    path: str,
    minimum: Decimal,
    maximum: Decimal,
) -> tuple[Decimal, Decimal, bool]:
    if isinstance(value, list):
        if len(value) != 2:
            raise ValidationError(f"{path} range must contain [low, high]")
        low = _bounded(value[0], f"{path}[0]", minimum, maximum)
        high = _bounded(value[1], f"{path}[1]", minimum, maximum)
        if low > high:
            raise ValidationError(f"{path} range low must not exceed high")
        return low, high, True
    point = _bounded(value, path, minimum, maximum)
    return point, point, False


def _nonempty_id(value: Any, path: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be a non-empty string")
    return value.strip()


def _evidence_ids(payload: dict[str, Any]) -> set[str]:
    records = payload.get("evidence")
    if not isinstance(records, list) or not records:
        raise ValidationError("evidence must be a non-empty list")
    identifiers: set[str] = set()
    for index, record in enumerate(records):
        if isinstance(record, str):
            identifier = _nonempty_id(record, f"evidence[{index}]")
        elif isinstance(record, dict):
            identifier = _nonempty_id(record.get("id"), f"evidence[{index}].id")
        else:
            raise ValidationError(f"evidence[{index}] must be an ID or object with id")
        if identifier in identifiers:
            raise ValidationError(f"duplicate evidence ID: {identifier}")
        identifiers.add(identifier)
    return identifiers


def _references(value: Any, path: str, known: set[str], required: bool = True) -> list[str]:
    if not isinstance(value, list):
        raise ValidationError(f"{path} must be a list")
    if required and not value:
        raise ValidationError(f"{path} must contain at least one evidence ID")
    result: list[str] = []
    seen: set[str] = set()
    for index, raw in enumerate(value):
        identifier = _nonempty_id(raw, f"{path}[{index}]")
        if identifier not in known:
            raise ValidationError(f"{path}[{index}] references unknown evidence ID {identifier}")
        if identifier in seen:
            raise ValidationError(f"{path} contains duplicate evidence ID {identifier}")
        seen.add(identifier)
        result.append(identifier)
    return sorted(result)


def _weights(value: Any, path: str, expected: set[str] | None = None) -> dict[str, Decimal]:
    if not isinstance(value, dict) or not value:
        raise ValidationError(f"{path} must be a non-empty object")
    result: dict[str, Decimal] = {}
    for raw_name, raw_weight in value.items():
        name = _nonempty_id(raw_name, f"{path} criterion")
        if name in result:
            raise ValidationError(f"{path} contains duplicate criterion {name}")
        result[name] = _bounded(raw_weight, f"{path}.{name}", Decimal("0"), WEIGHT_TOTAL)
    if sum(result.values(), Decimal("0")) != WEIGHT_TOTAL:
        raise ValidationError(f"{path} must sum to 100")
    if expected is not None and set(result) != expected:
        missing = sorted(expected - set(result))
        extra = sorted(set(result) - expected)
        raise ValidationError(f"{path} criteria mismatch; missing={missing}, extra={extra}")
    return dict(sorted(result.items()))


def _rounded(value: Decimal) -> float:
    return float(value.quantize(Decimal("0.0001")))


def _metric(
    score_records: dict[str, dict[str, Any]],
    weights: dict[str, Decimal],
) -> dict[str, Any]:
    low = Decimal("0")
    high = Decimal("0")
    confidence_low = Decimal("0")
    confidence_high = Decimal("0")
    has_range = False
    for criterion, weight in weights.items():
        record = score_records[criterion]
        score_low, score_high, score_range = record["score_range"]
        conf_low, conf_high, conf_range = record["confidence_range"]
        factor = weight / WEIGHT_TOTAL
        low += score_low * factor
        high += score_high * factor
        confidence_low += conf_low * factor
        confidence_high += conf_high * factor
        has_range = has_range or score_range or conf_range
    midpoint = (low + high) / Decimal("2")
    confidence = (confidence_low + confidence_high) / Decimal("2")
    return {
        "confidence": _rounded(confidence),
        "confidence_range": [_rounded(confidence_low), _rounded(confidence_high)],
        "has_range": has_range,
        "score": _rounded(midpoint),
        "score_range": [_rounded(low), _rounded(high)],
    }


def _winner(
    metrics: dict[str, dict[str, Any]],
    eligible: set[str],
    tolerance: Decimal,
) -> tuple[str | None, list[str], bool]:
    order = sorted(
        eligible,
        key=lambda identifier: (-Decimal(str(metrics[identifier]["score"])), identifier),
    )
    if not order:
        return None, [], False
    if len(order) == 1:
        return order[0], order, False
    first = Decimal(str(metrics[order[0]]["score"]))
    second = Decimal(str(metrics[order[1]]["score"]))
    tied = first - second <= tolerance
    return (None if tied else order[0]), order, tied


def score_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Validate and deterministically score an explicit assessment payload."""
    if not isinstance(payload, dict):
        raise ValidationError("input must be a JSON object")

    known_evidence = _evidence_ids(payload)
    base_weights = _weights(payload.get("weights"), "weights")
    criteria = set(base_weights)
    tolerance = _bounded(
        payload.get("tie_tolerance", 0),
        "tie_tolerance",
        Decimal("0"),
        SCORE_MAX - SCORE_MIN,
    )
    minimum_confidence: Decimal | None = None
    if "minimum_confidence" in payload:
        minimum_confidence = _bounded(
            payload["minimum_confidence"],
            "minimum_confidence",
            CONFIDENCE_MIN,
            CONFIDENCE_MAX,
        )

    raw_scenarios = payload.get("sensitivity_scenarios", [])
    if not isinstance(raw_scenarios, list):
        raise ValidationError("sensitivity_scenarios must be a list")
    scenarios: dict[str, dict[str, Decimal]] = {}
    for index, scenario in enumerate(raw_scenarios):
        if not isinstance(scenario, dict):
            raise ValidationError(f"sensitivity_scenarios[{index}] must be an object")
        name = _nonempty_id(scenario.get("name"), f"sensitivity_scenarios[{index}].name")
        if name == "base" or name in scenarios:
            raise ValidationError(f"duplicate or reserved sensitivity scenario name: {name}")
        scenarios[name] = _weights(
            scenario.get("weights"),
            f"sensitivity_scenarios[{index}].weights",
            criteria,
        )

    raw_opportunities = payload.get("opportunities")
    if not isinstance(raw_opportunities, list) or not raw_opportunities:
        raise ValidationError("opportunities must be a non-empty list")

    parsed: dict[str, dict[str, Any]] = {}
    for index, opportunity in enumerate(raw_opportunities):
        path = f"opportunities[{index}]"
        if not isinstance(opportunity, dict):
            raise ValidationError(f"{path} must be an object")
        identifier = _nonempty_id(opportunity.get("id"), f"{path}.id")
        if identifier in parsed:
            raise ValidationError(f"duplicate opportunity ID: {identifier}")
        name = _nonempty_id(opportunity.get("name", identifier), f"{path}.name")

        raw_scores = opportunity.get("scores")
        if not isinstance(raw_scores, dict):
            raise ValidationError(f"{path}.scores must be an object")
        if set(raw_scores) != criteria:
            missing = sorted(criteria - set(raw_scores))
            extra = sorted(set(raw_scores) - criteria)
            raise ValidationError(f"{path}.scores criteria mismatch; missing={missing}, extra={extra}")
        score_records: dict[str, dict[str, Any]] = {}
        public_scores: dict[str, Any] = {}
        for criterion in sorted(criteria):
            record = raw_scores[criterion]
            score_path = f"{path}.scores.{criterion}"
            if not isinstance(record, dict):
                raise ValidationError(f"{score_path} must be an object")
            score_range = _range(record.get("score"), f"{score_path}.score", SCORE_MIN, SCORE_MAX)
            confidence_range = _range(
                record.get("confidence"),
                f"{score_path}.confidence",
                CONFIDENCE_MIN,
                CONFIDENCE_MAX,
            )
            refs = _references(record.get("evidence_ids"), f"{score_path}.evidence_ids", known_evidence)
            score_records[criterion] = {
                "score_range": score_range,
                "confidence_range": confidence_range,
            }
            public_scores[criterion] = {
                "confidence": record["confidence"],
                "evidence_ids": refs,
                "score": record["score"],
            }

        raw_gates = opportunity.get("fatal_gates")
        if not isinstance(raw_gates, dict) or not raw_gates:
            raise ValidationError(f"{path}.fatal_gates must be a non-empty object")
        if "first_customer_path" not in raw_gates:
            raise ValidationError(f"{path}.fatal_gates must include first_customer_path")
        gates: dict[str, Any] = {}
        failed: list[str] = []
        unknown: list[str] = []
        for gate_name in sorted(raw_gates):
            gate = raw_gates[gate_name]
            gate_path = f"{path}.fatal_gates.{gate_name}"
            if not isinstance(gate, dict):
                raise ValidationError(f"{gate_path} must be an object")
            status = gate.get("status")
            if status not in GATE_STATUSES:
                raise ValidationError(f"{gate_path}.status must be pass, fail, or unknown")
            refs = _references(
                gate.get("evidence_ids", []),
                f"{gate_path}.evidence_ids",
                known_evidence,
                required=status != "unknown",
            )
            reason = gate.get("reason", "")
            if reason is not None and not isinstance(reason, str):
                raise ValidationError(f"{gate_path}.reason must be a string")
            gates[gate_name] = {"evidence_ids": refs, "reason": reason or "", "status": status}
            if status == "fail":
                failed.append(gate_name)
            elif status == "unknown":
                unknown.append(gate_name)

        parsed[identifier] = {
            "failed_gates": failed,
            "fatal_gates": gates,
            "name": name,
            "public_scores": public_scores,
            "score_records": score_records,
            "unknown_gates": unknown,
        }

    eligible = {
        identifier
        for identifier, opportunity in parsed.items()
        if not opportunity["failed_gates"] and not opportunity["unknown_gates"]
    }
    metric_sets: dict[str, dict[str, dict[str, Any]]] = {"base": {}}
    for identifier in eligible:
        metric_sets["base"][identifier] = _metric(parsed[identifier]["score_records"], base_weights)
    for scenario_name, scenario_weights in sorted(scenarios.items()):
        metric_sets[scenario_name] = {
            identifier: _metric(parsed[identifier]["score_records"], scenario_weights)
            for identifier in eligible
        }
    base_winner, base_order, base_tied = _winner(metric_sets["base"], eligible, tolerance)
    scenario_winners: dict[str, str | None] = {}
    scenario_ties: dict[str, bool] = {}
    scenario_overlaps: dict[str, bool] = {}
    for scenario_name in sorted(scenarios):
        winner, order, tied = _winner(metric_sets[scenario_name], eligible, tolerance)
        scenario_winners[scenario_name] = winner
        scenario_ties[scenario_name] = tied
        if len(order) >= 2:
            leader_low = Decimal(str(metric_sets[scenario_name][order[0]]["score_range"][0]))
            runner_high = Decimal(str(metric_sets[scenario_name][order[1]]["score_range"][1]))
            scenario_overlaps[scenario_name] = leader_low <= runner_high
        else:
            scenario_overlaps[scenario_name] = False

    status: str
    reason: str
    winner_id: str | None = base_winner
    if len(eligible) < 2:
        status = "insufficient"
        winner_id = None
        reason = "ranking requires at least two opportunities that pass every fatal gate"
    elif base_tied:
        status = "tied"
        reason = "the leading base scores are within the explicit tie tolerance"
    elif minimum_confidence is not None and Decimal(str(metric_sets["base"][base_order[0]]["confidence"])) < minimum_confidence:
        status = "insufficient"
        winner_id = None
        reason = "the leading opportunity is below the explicit minimum confidence"
    else:
        top = base_order[0]
        runner_up = base_order[1]
        top_low = Decimal(str(metric_sets["base"][top]["score_range"][0]))
        runner_high = Decimal(str(metric_sets["base"][runner_up]["score_range"][1]))
        interval_overlap = top_low <= runner_high
        scenario_changed = any(
            tied or scenario_winners[name] != top
            for name, tied in scenario_ties.items()
        )
        sensitivity_overlap = any(scenario_overlaps.values())
        if interval_overlap or scenario_changed or sensitivity_overlap:
            status = "fragile"
            reasons: list[str] = []
            if interval_overlap:
                reasons.append("leading score ranges overlap")
            if scenario_changed:
                reasons.append("the winner changes or ties under a sensitivity scenario")
            if sensitivity_overlap:
                reasons.append("leading score ranges overlap under a sensitivity scenario")
            reason = "; ".join(reasons)
        else:
            status = "robust"
            reason = "the same unique winner leads without range overlap in every supplied scenario"

    opportunities_output: list[dict[str, Any]] = []
    for identifier in sorted(parsed):
        opportunity = parsed[identifier]
        opportunities_output.append(
            {
                "eligible": identifier in eligible,
                "failed_gates": opportunity["failed_gates"],
                "fatal_gates": opportunity["fatal_gates"],
                "id": identifier,
                "name": opportunity["name"],
                "scores": {
                    "base": metric_sets["base"].get(identifier),
                    "criteria": opportunity["public_scores"],
                    "scenarios": {
                        name: metric_sets[name][identifier]
                        for name in sorted(scenarios)
                        if identifier in metric_sets[name]
                    },
                },
                "unknown_gates": opportunity["unknown_gates"],
            }
        )

    return {
        "criteria": sorted(criteria),
        "opportunities": opportunities_output,
        "ranking": {
            "base_order": base_order,
            "eligible_ids": sorted(eligible),
            "leading_id": base_order[0] if base_order else None,
            "reason": reason,
            "scenario_winners": scenario_winners,
            "scenario_range_overlaps": scenario_overlaps,
            "status": status,
            "winner_id": winner_id,
        },
        "weights": {
            "base": {key: _rounded(value) for key, value in base_weights.items()},
            "scenarios": {
                name: {key: _rounded(value) for key, value in weights.items()}
                for name, weights in sorted(scenarios.items())
            },
        },
    }


def _load(path: str) -> dict[str, Any]:
    stream = sys.stdin if path == "-" else open(path, "r", encoding="utf-8")
    try:
        return json.load(stream)
    finally:
        if stream is not sys.stdin:
            stream.close()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", default="-", help="JSON file, or - for stdin")
    args = parser.parse_args(argv)
    try:
        result = score_payload(_load(args.input))
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"error": str(exc), "valid": False}, ensure_ascii=False, sort_keys=True), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

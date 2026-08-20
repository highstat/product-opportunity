#!/usr/bin/env python3
"""Validate a portable product-opportunity evidence and experiment packet."""

from __future__ import annotations

import argparse
from datetime import date
import json
import sys
from typing import Any
from urllib.parse import urlparse


CLAIM_STATUSES = {"Fact", "Inference", "Hypothesis", "Unknown"}
CURRENT_TOPICS = {"price", "policy", "competitor"}
GATE_STATUSES = {"pass", "fail", "unknown"}
BOUNDARY_STATUSES = {"Closed", "Limited evidence-bearing slice", "Open for specified scope"}
ROUTE_STATUSES = {"Evidenced", "Conditional", "Unknown"}


def _valid_url(value: Any) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def _date(value: Any) -> date | None:
    if not isinstance(value, str):
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _criteria_present(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(item, str) and item.strip() for item in value)
    return False


def validate_packet(packet: Any) -> dict[str, Any]:
    """Return deterministic structured errors without mutating the packet."""
    errors: list[dict[str, str]] = []

    def add(code: str, path: str, message: str) -> None:
        errors.append({"code": code, "message": message, "path": path})

    if not isinstance(packet, dict):
        add("type", "$", "packet must be a JSON object")
        return {"errors": errors, "valid": False}

    as_of = _date(packet.get("as_of"))
    if as_of is None:
        add("date", "as_of", "as_of must be an ISO date (YYYY-MM-DD)")

    evidence_by_id: dict[str, dict[str, Any]] = {}
    evidence = packet.get("evidence")
    if not isinstance(evidence, list):
        add("type", "evidence", "evidence must be a list")
        evidence = []
    for index, record in enumerate(evidence):
        path = f"evidence[{index}]"
        if not isinstance(record, dict):
            add("type", path, "evidence record must be an object")
            continue
        identifier = record.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            add("required", f"{path}.id", "evidence ID is required")
            continue
        identifier = identifier.strip()
        if identifier in evidence_by_id:
            add("duplicate", f"{path}.id", f"duplicate evidence ID {identifier}")
            continue
        evidence_by_id[identifier] = record
        if not isinstance(record.get("origin_id"), str) or not record["origin_id"].strip():
            add("origin", f"{path}.origin_id", "origin_id is required for independence checks")

    claims = packet.get("claims")
    if not isinstance(claims, list):
        add("type", "claims", "claims must be a list")
        claims = []
    seen_claims: set[str] = set()
    for index, claim in enumerate(claims):
        path = f"claims[{index}]"
        if not isinstance(claim, dict):
            add("type", path, "claim must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id.strip():
            add("required", f"{path}.id", "claim ID is required")
        elif claim_id in seen_claims:
            add("duplicate", f"{path}.id", f"duplicate claim ID {claim_id}")
        else:
            seen_claims.add(claim_id)
        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            add("enum", f"{path}.status", "status must be Fact, Inference, Hypothesis, or Unknown")
        if not isinstance(claim.get("statement"), str) or not claim["statement"].strip():
            add("required", f"{path}.statement", "claim statement is required")
        refs = claim.get("evidence_ids", [])
        if not isinstance(refs, list):
            add("type", f"{path}.evidence_ids", "evidence_ids must be a list")
            refs = []
        if status == "Fact" and not refs:
            add("fact-evidence", f"{path}.evidence_ids", "Fact must cite at least one evidence ID")
        resolved: list[tuple[str, dict[str, Any]]] = []
        for ref_index, identifier in enumerate(refs):
            ref_path = f"{path}.evidence_ids[{ref_index}]"
            if not isinstance(identifier, str) or identifier not in evidence_by_id:
                add("evidence-ref", ref_path, f"unknown evidence ID {identifier!r}")
                continue
            resolved.append((identifier, evidence_by_id[identifier]))
            if status == "Fact" and not _valid_url(evidence_by_id[identifier].get("url")):
                add("fact-url", ref_path, "evidence supporting a Fact must have an http(s) URL")

        current_topics = {
            str(claim.get("topic", "other")),
            *(str(record.get("evidence_type", "other")) for _, record in resolved),
        } & CURRENT_TOPICS
        if current_topics and status == "Fact":
            dated = False
            for identifier, record in resolved:
                if record.get("evidence_type") not in current_topics and claim.get("topic") not in current_topics:
                    continue
                source_date = _date(record.get("published_or_updated"))
                retrieved_at = _date(record.get("retrieved"))
                if source_date is not None and retrieved_at is not None:
                    dated = True
                    if as_of is not None and (source_date > as_of or retrieved_at > as_of):
                        add(
                            "future-date",
                            f"evidence[{identifier}]",
                            "source and retrieval dates must not be later than as_of",
                        )
            if not dated:
                add(
                    "current-date",
                    f"{path}.evidence_ids",
                    "current price/policy/competitor Fact needs evidence with published_or_updated and retrieved",
                )

    blocker_paths: list[str] = []
    opportunities = packet.get("opportunities")
    if not isinstance(opportunities, list):
        add("type", "opportunities", "opportunities must be a list")
        opportunities = []
    seen_opportunities: set[str] = set()
    for index, opportunity in enumerate(opportunities):
        path = f"opportunities[{index}]"
        if not isinstance(opportunity, dict):
            add("type", path, "opportunity must be an object")
            continue
        identifier = opportunity.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            add("required", f"{path}.id", "opportunity ID is required")
        elif identifier in seen_opportunities:
            add("duplicate", f"{path}.id", f"duplicate opportunity ID {identifier}")
        else:
            seen_opportunities.add(identifier)

        route = opportunity.get("first_customer_route")
        route_status: str | None = None
        if not isinstance(route, dict):
            add("required", f"{path}.first_customer_route", "first_customer_route object is required")
        else:
            route_status = route.get("status")
            if route_status not in ROUTE_STATUSES:
                add(
                    "enum",
                    f"{path}.first_customer_route.status",
                    "status must be Evidenced, Conditional, or Unknown",
                )
            if not isinstance(route.get("summary"), str) or not route["summary"].strip():
                add("required", f"{path}.first_customer_route.summary", "route summary is required")
            route_refs = route.get("evidence_ids", [])
            if not isinstance(route_refs, list):
                add("type", f"{path}.first_customer_route.evidence_ids", "evidence_ids must be a list")
                route_refs = []
            if route_status == "Evidenced" and not route_refs:
                add(
                    "route-evidence",
                    f"{path}.first_customer_route.evidence_ids",
                    "an Evidenced route must cite evidence IDs",
                )
            for ref_index, evidence_id in enumerate(route_refs):
                if evidence_id not in evidence_by_id:
                    add(
                        "evidence-ref",
                        f"{path}.first_customer_route.evidence_ids[{ref_index}]",
                        f"unknown evidence ID {evidence_id!r}",
                    )

        scores = opportunity.get("scores")
        if not isinstance(scores, dict) or not scores:
            add("required", f"{path}.scores", "scores must be a non-empty object")
            scores = {}
        for criterion, score in sorted(scores.items()):
            score_path = f"{path}.scores.{criterion}"
            if not isinstance(score, dict):
                add("type", score_path, "score must be an object")
                continue
            refs = score.get("evidence_ids")
            if not isinstance(refs, list) or not refs:
                add("score-evidence", f"{score_path}.evidence_ids", "every score must cite evidence IDs")
                continue
            for ref_index, evidence_id in enumerate(refs):
                if evidence_id not in evidence_by_id:
                    add(
                        "evidence-ref",
                        f"{score_path}.evidence_ids[{ref_index}]",
                        f"unknown evidence ID {evidence_id!r}",
                    )

        gates = opportunity.get("fatal_gates")
        if not isinstance(gates, dict) or not gates:
            add("required", f"{path}.fatal_gates", "fatal_gates must be a non-empty object")
            gates = {}
        if "first_customer_path" not in gates:
            add(
                "required",
                f"{path}.fatal_gates.first_customer_path",
                "first_customer_path fatal gate is required",
            )
        for gate_name, gate in sorted(gates.items()):
            gate_path = f"{path}.fatal_gates.{gate_name}"
            if not isinstance(gate, dict):
                add("type", gate_path, "fatal gate must be an object")
                continue
            status = gate.get("status")
            if status not in GATE_STATUSES:
                add("enum", f"{gate_path}.status", "status must be pass, fail, or unknown")
            elif status in {"fail", "unknown"}:
                blocker_paths.append(gate_path)
            refs = gate.get("evidence_ids", [])
            if not isinstance(refs, list):
                add("type", f"{gate_path}.evidence_ids", "evidence_ids must be a list")
            else:
                if status in {"pass", "fail"} and not refs:
                    add(
                        "gate-evidence",
                        f"{gate_path}.evidence_ids",
                        "passed or failed fatal gate must cite evidence IDs",
                    )
                for ref_index, evidence_id in enumerate(refs):
                    if evidence_id not in evidence_by_id:
                        add(
                            "evidence-ref",
                            f"{gate_path}.evidence_ids[{ref_index}]",
                            f"unknown evidence ID {evidence_id!r}",
                        )

        route_gate = gates.get("first_customer_path")
        if isinstance(route_gate, dict) and route_gate.get("status") in GATE_STATUSES:
            route_gate_status = route_gate["status"]
            if route_status == "Evidenced" and route_gate_status != "pass":
                add(
                    "route-gate",
                    f"{path}.fatal_gates.first_customer_path.status",
                    "an Evidenced route requires a passed first_customer_path gate",
                )
            if route_status in {"Conditional", "Unknown"} and route_gate_status == "pass":
                add(
                    "route-gate",
                    f"{path}.fatal_gates.first_customer_path.status",
                    "a Conditional or Unknown route cannot pass the first_customer_path gate",
                )

    boundary = packet.get("build_boundary")
    if not isinstance(boundary, dict):
        add("required", "build_boundary", "build_boundary object is required")
    else:
        boundary_status = boundary.get("status")
        if boundary_status not in BOUNDARY_STATUSES:
            add(
                "enum",
                "build_boundary.status",
                "status must be Closed, Limited evidence-bearing slice, or Open for specified scope",
            )
        elif blocker_paths and boundary_status != "Closed":
            add(
                "build-boundary",
                "build_boundary.status",
                "build boundary must be closed while any fatal gate is failed or unknown",
            )

    independence = packet.get("independence_claims", [])
    if not isinstance(independence, list):
        add("type", "independence_claims", "independence_claims must be a list")
        independence = []
    for index, claim in enumerate(independence):
        path = f"independence_claims[{index}]"
        if not isinstance(claim, dict):
            add("type", path, "independence claim must be an object")
            continue
        refs = claim.get("evidence_ids")
        if not isinstance(refs, list) or len(refs) < 2:
            add("independence", f"{path}.evidence_ids", "independence claim needs at least two evidence IDs")
            continue
        records: list[dict[str, Any]] = []
        for ref_index, identifier in enumerate(refs):
            if identifier not in evidence_by_id:
                add(
                    "evidence-ref",
                    f"{path}.evidence_ids[{ref_index}]",
                    f"unknown evidence ID {identifier!r}",
                )
            else:
                records.append(evidence_by_id[identifier])
        independent = claim.get("independent")
        if not isinstance(independent, bool):
            add("type", f"{path}.independent", "independent must be boolean")
        elif independent:
            if not isinstance(claim.get("basis"), str) or not claim["basis"].strip():
                add("independence-basis", f"{path}.basis", "positive independence claim needs a basis")
            origins = [record.get("origin_id") for record in records]
            if len(records) == len(refs) and len(set(origins)) != len(origins):
                add(
                    "same-origin",
                    f"{path}.evidence_ids",
                    "evidence sharing an origin_id cannot be claimed as independent",
                )

    experiments = packet.get("experiments")
    if not isinstance(experiments, list):
        add("type", "experiments", "experiments must be a list")
        experiments = []
    seen_experiments: set[str] = set()
    for index, experiment in enumerate(experiments):
        path = f"experiments[{index}]"
        if not isinstance(experiment, dict):
            add("type", path, "experiment must be an object")
            continue
        identifier = experiment.get("id")
        if not isinstance(identifier, str) or not identifier.strip():
            add("required", f"{path}.id", "experiment ID is required")
        elif identifier in seen_experiments:
            add("duplicate", f"{path}.id", f"duplicate experiment ID {identifier}")
        else:
            seen_experiments.add(identifier)
        if not isinstance(experiment.get("hypothesis"), str) or not experiment["hypothesis"].strip():
            add("required", f"{path}.hypothesis", "experiment hypothesis is required")
        for field in ("success", "failure", "inconclusive"):
            if not _criteria_present(experiment.get(field)):
                add(
                    "experiment-outcome",
                    f"{path}.{field}",
                    f"{field} must be a non-empty string or list of strings",
                )

    errors.sort(key=lambda item: (item["path"], item["code"], item["message"]))
    return {
        "errors": errors,
        "summary": {
            "blocking_fatal_gates": sorted(blocker_paths),
            "claims": len(claims),
            "evidence_records": len(evidence_by_id),
            "experiments": len(experiments),
            "opportunities": len(opportunities),
        },
        "valid": not errors,
    }


def _load(path: str) -> Any:
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
        packet = _load(args.input)
    except (OSError, json.JSONDecodeError) as exc:
        result = {"errors": [{"code": "input", "message": str(exc), "path": "$"}], "valid": False}
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 2
    result = validate_packet(packet)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

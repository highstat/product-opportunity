# Experiment learning and portable state

Use this in `validate` and `review-results`. Do not rely on hidden chat memory. Maintain an append-only, portable state so another task can audit what was believed, tested, and changed.

## Stable IDs

- `O1`: opportunity
- `A1`: assumption
- `E1`: evidence
- `X1`: experiment
- `D1`: decision

Never overwrite an earlier record. Add a new version or decision that references the superseded item. Preserve unfavorable evidence.

## Minimal case state

```yaml
case_id: short-stable-name
objective: User decision objective and horizon
constraints: Skills, access, budget, time, geography, risk
opportunities: []
assumptions: []
evidence: []
experiments: []
decisions: []
current_bottleneck: A1
next_allowed_action: Research or experiment only
build_boundary: Closed | Limited evidence-bearing slice | Open for specified scope
```

An experiment result appends:

```yaml
id: X1-result
experiment_id: X1
run_date: YYYY-MM-DD
planned_segment: ...
actual_segment: ...
planned_channel: ...
actual_channel: ...
exposure_denominator: ...
observed_behavior: ...
refusal_reasons: ...
deviations: ...
validity_threats: ...
outcome: supported | weakened | falsified | inconclusive | invalid-test
evidence_delta: [E7]
affected_assumptions: [A1]
decision_delta: D2
```

## Review-results procedure

1. Recover the precommitted hypothesis, segment, channel, instrument, denominator, success, failure, and inconclusive rules.
2. Compare plan with execution. If missing, label the limitation; do not invent a precommitment after seeing results.
3. Determine whether channel, recruitment, qualification, message, instrumentation, or delivery failure prevents interpretation.
4. Classify the outcome. Separate “we learned the hypothesis is weak” from “the test could not observe it.”
5. Add result evidence with scope and limitations. Update only claims the experiment can support.
6. Preserve the original record and all negative evidence. Never reinterpret an old failure solely to fit a new narrative.
7. Re-run only affected gates, score ranges, and risks.
8. Record a new decision: `continue`, `revise segment`, `revise hypothesis`, `rerun valid test`, or `stop`.
9. Name the new decision bottleneck and one next experiment, or explain why no further test is justified.

## Outcome meanings

- `supported`: met the precommitted success condition with a valid test; scope support narrowly.
- `weakened`: useful negative evidence, but not enough to reject the assumption.
- `falsified`: a valid test met the precommitted failure condition for the stated scope.
- `inconclusive`: valid observations exist but exposure, power, or ambiguity prevents the planned decision.
- `invalid-test`: execution or measurement failure means the intended assumption was not tested.

Do not equate `inconclusive` with weak demand or `invalid-test` with no demand. Do not equate `supported` with product-market fit.

## Segment changes

When evidence points to a different segment:

- keep the negative evidence against the original segment;
- create a new assumption for the new segment;
- treat unsolicited requests or commitments as evidence, not automatic validation;
- test the new payer, workflow, and route separately.

## Compact state delta

In normal output, show only:

```text
Added: E7, X2-result, D3
Changed: A2 supported for [narrow scope]; R1 reduced/increased
Unchanged: prior negative E1/E4; build boundary
Next bottleneck: A3
Next action: X3 or stop
```

Offer the full portable state block when the user needs to continue in another task. Never require proprietary storage or a paid service.

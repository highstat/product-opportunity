# Cheapest adequate validation experiment

Use this in `validate` and `review-results`. The objective is one experiment that can change the next decision, not a generic validation checklist.

## Start with the decision bottleneck

Write:

> We cannot decide `[decision]` until we learn whether `[riskiest assumption]` for `[specific segment/situation]` is sufficiently true.

Do not test message, usability, feasibility, and willingness to pay at once. Choose the assumption whose resolution can unlock, reframe, or kill the opportunity.

## Candidate experiment map

Generate only plausible candidates for that assumption:

| Assumption | Useful experiment patterns |
|---|---|
| Problem occurs and matters | Recent-behavior interviews, workflow observation, artifact/support-log review |
| Audience can be reached | Small permitted prospect-surface/reply test with qualification and denominator |
| Willingness to pay | Paid manual service, paid pilot, transparent refundable deposit, procurement/budget step |
| Outcome can be delivered | Concierge workflow using real inputs and acceptance criteria |
| User will switch/adopt | Realistic migration or task test with current alternative present |
| Offer/message resonates | Transparent offer or landing CTA after the problem/channel is credible |
| Technical feasibility | Narrow technical spike only when feasibility is the decision bottleneck |
| Legal/platform permission | Current primary-policy/legal check; this is a gate, not a demand test |

A/B testing usually requires enough traffic and is rarely the first test for a user without an audience. A prototype is not automatically an MVP; build it only when interaction evidence cannot be obtained more cheaply.

## Select the cheapest adequate test

Compare candidates ordinally; do not invent exact information-value numbers. Eliminate a test when another costs no more, is no riskier, and provides stronger or less ambiguous evidence for the same decision.

Assess:

- can a negative result falsify or materially weaken the assumption?
- how strong is a positive result for this exact claim?
- how ambiguous is a negative result?
- can the relevant segment be recruited through a permitted route?
- is the exposure denominator observable?
- what are maximum cash, founder time, and calendar time?
- is the test reversible?
- what legal, platform, privacy, security, refund, and reputation risk exists?
- what decision follows from pass, fail, and inconclusive outcomes?

Prefer the least costly surviving test. “Cheapest” without adequacy is waste; “strongest possible” may be unnecessary.

## Experiment card

```yaml
id: X1
decision: Decision this test can change
assumption_id: A1
hypothesis: Specific segment, situation, offer, and behavior
segment: Inclusion and exclusion criteria
channel: Current surface and permitted access method
instrument: Interview, manual service, offer, deposit, prototype, or concierge flow
cta: Observable requested action
denominator: Who is exposed and how counted
max_cash: Amount and currency
founder_time: Maximum hours
timebox: Start/end or duration
success: Precommitted observable threshold and resulting decision
failure: Precommitted threshold and resulting decision
inconclusive: Conditions that invalidate or underpower interpretation; resulting action
safeguards: Legal, platform, privacy, security, refund, and disclosure controls
expected_strength: Which claim the result could support and its limitations
```

Thresholds must follow the decision, attainable exposure, economics, and downside. Do not use universal interview counts, CTR, signup, CPL, or conversion benchmarks.

## Truthful commercial tests

- State clearly when the product does not yet exist or delivery is manual.
- Describe scope, timing, refund, and data handling honestly.
- Use established payment providers; do not collect card details directly.
- Obtain required consent and minimize stored data.
- Do not create fake scarcity, testimonials, customers, guarantees, or functionality.
- Do not run or publish the experiment without separate user authorization.

## Interpreting results

Audit validity before the hypothesis:

- Was the intended segment actually exposed?
- Was the channel functioning and permitted?
- Was the ask understood and technically measurable?
- Did the test follow its precommitment?
- Did external events or selection bias dominate?

Classify the result `supported`, `weakened`, `falsified`, `inconclusive`, or `invalid test`. A broken email domain does not falsify demand. A paid pilot supports one offer/segment but does not prove retention or scalable acquisition.

Use [experiment-learning.md](experiment-learning.md) to update state and select the next bottleneck.

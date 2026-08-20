# Scoring and robust comparison

Use scoring only after fatal gates. A score is a transparent comparison under stated objectives, not a success probability, revenue forecast, or substitute for missing evidence.

## Four-layer decision

1. **Fatal gates:** reachability, problem significance, sufficient free alternative, required access/trust/capital/license, proportional economics, and unacceptable legal/platform/privacy/security/ethical downside.
2. **Opportunity evidence:** problem strength, urgency/frequency, existing spend or costly workaround, dissatisfaction, switching trigger, and payment behavior.
3. **Founder path fit:** first-buyer reachability, trust, time to evidence, skill fit, delivery/support load, geography/language, and reversibility.
4. **Coverage/confidence:** how much of the important judgment is directly supported and how applicable the evidence is.

Do not calculate a weighted total for an opportunity with a failed fatal gate. An unresolved fatal unknown keeps the build boundary closed and normally makes ranking provisional.

## Define criteria from the user's objective

State the decision objective before assigning weights. Examples:

- first $100 soon: reachability, time to transaction evidence, low test cost, and delivery fit dominate;
- specialist B2B access: pain, budget ownership, channel access, trust, and paid-pilot feasibility dominate;
- low-maintenance income: recurring value, retention evidence, support, abuse, and dependency risk dominate.

Weights are value judgments. Explain them briefly and keep them consistent across candidates. Do not import universal weights or benchmarks.

## Anchored scores and ranges

Use a small ordinal scale, usually `0–4`, with criterion-specific anchors. Example for first-buyer reachability:

- `0`: no permitted plausible route;
- `1`: audience exists, access/trust largely unknown;
- `2`: a current surface and permitted research route exist;
- `3`: qualified prospects and a credible offer route exist;
- `4`: the user has recently reached comparable buyers or obtained commitment.

Document anchors for every criterion used. Each rating needs evidence IDs and a confidence from `0–1` describing support quality, not probability of success.

When evidence supports a range, keep `[low, high]`. `Unknown` is a range implied by the anchors, not a hidden zero or midpoint. Use `N/A` only when a criterion truly does not apply to the comparison; remove that criterion for every candidate and renormalize weights transparently.

## Arithmetic

For exact scores, weighted total is:

`sum(weight × score) / sum(weight)`

Report on the original score scale. Keep evidence-weighted support separate, for example:

`sum(weight × confidence) / sum(weight)`

Do not multiply total score by confidence and present the product as a probability.

For ranges, calculate low and high totals from supplied bounds. Use the deterministic script when helpful.

## Sensitivity and dominance

Test reasonable weight scenarios derived from plausible variants of the user's goal, plus material unknown ranges. Classify:

- `robust winner`: wins across all reasonable scenarios and material ranges;
- `fragile winner`: leads in the base case but another candidate wins under a reasonable scenario;
- `effectively tied`: differences are smaller than the judgment/evidence resolution;
- `insufficient evidence to rank`: fatal unknowns or ranges are too broad.

If one candidate's plausible low score exceeds another's plausible high score, it dominates on supplied assumptions. If intervals overlap or the winner flips, do not force a precise ranking. Choose the experiment that resolves the discriminating unknown.

## Recommended criteria library

Select only criteria relevant to the objective:

- observed problem consequence;
- urgency and frequency;
- existing spend/costly workaround;
- dissatisfaction and switching trigger;
- payer and budget clarity;
- research/sales reachability;
- trust and sales friction;
- time and cash to evidence;
- implementation/delivery fit;
- onboarding/support/operations load;
- plausible unit-economics range;
- platform/legal/privacy/security risk;
- reversibility and downside.

Avoid double-counting the same evidence under near-duplicate criteria. Market size is rarely decisive for a first-customer objective; use reachable segment and achievable transaction instead.

## Output table

Show:

| Opportunity | Gates | Weighted range | Evidence support | Stability | Key reason | Discriminating unknown |
|---|---|---:|---:|---|---|---|

Round for readability. More decimals do not make judgments more accurate. Follow with the weight rationale, critical anchors, and sensitivity conclusion—not a full spreadsheet dump.

## Script contract

`scripts/score_opportunities.py` performs arithmetic on supplied JSON. The model or researcher owns criterion choice, anchors, semantic ratings, evidence linkage, and verdict. Reject script output when its inputs violate the evidence record or fatal gates.

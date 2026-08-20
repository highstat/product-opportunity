# Output contract

Put the decision first. Include detail only when it can change or audit the decision. Do not produce a consultant-style report by default.

## Default Decision Card

```markdown
## Decision

- Discovery result: No candidate yet | Candidate(s) survive [discover only; omit after selecting a candidate]
- Opportunity: Reject | Reframe | Validate | Evidence-supported
- Confidence: low | medium | high — one sentence on evidence coverage
- Build boundary: Closed | Limited evidence-bearing slice | Open for [specified scope]
- Decision bottleneck: [one assumption]
- Strongest for: [claim + evidence IDs]
- Strongest against: [claim + evidence IDs]
- First-customer route: [buyer → trigger → surface → permitted access → trust bridge → ask]
- Route status: Evidenced | Conditional | Unknown — [current source and checked date, or missing proof]
- Next experiment: [one line]
- Limit: [cash, founder hours, timebox]
- Success: [behavior → decision]
- Failure: [behavior → decision]
- Inconclusive: [condition → decision]
- Critical unknowns: [short list]
```

If no customer route is evidenced, say so in the card instead of fabricating one. If the build boundary is limited, state both the permitted evidence-bearing artifact and the forbidden broader scope.

In `discover`, when no complete opportunity unit survives, use `Discovery result: No candidate yet`; omit the opportunity verdict and score. `Next experiment` may be `None for the current framing` after `Reject`; do not invent a test that reopens an unacceptable gate. A safe adjacent probe must be labeled as a separate reframed opportunity.

## Mode-specific body

### `discover`

After the card, include:

1. context and constraints;
2. observable channel/problem signals;
3. up to three surviving opportunities;
4. detailed leading opportunity and alternatives;
5. evidence gaps and sources.

Comparison table:

| Rank | Opportunity | First-buyer route | Gates | Score range/support | Strongest for | Strongest against | Riskiest unknown |
|---:|---|---|---|---|---|---|---|

Return fewer than three when evidence supports fewer.

### `evaluate`

Show the opportunity thesis, current behavior and alternatives, first-customer route, fatal gates, evidence for/against, risks, and next decision. Do not force a market-size section if it does not matter.

### `compare`

Show the objective and weight rationale, gated comparison, score ranges/evidence support, sensitivity conclusion, discriminating unknown, and recommended experiment. Say `fragile`, `tied`, or `insufficient` when appropriate.

### `validate`

Show the bottleneck, candidate tests considered, why dominated tests were rejected, the selected experiment card, safeguards, and the portable state additions. One experiment is the default.

### `review-results`

Do not regenerate the full market report. Show:

1. validity audit;
2. outcome classification;
3. evidence/assumption/risk/score delta;
4. opportunity verdict and build-boundary delta;
5. next bottleneck and next action;
6. compact portable state delta.

## Evidence appendix

Include only material records:

| ID | Status/type | Claim or evidence | Source/date | Supports/contradicts | Limitations |
|---|---|---|---|---|---|

Current external claims require clickable source links and dates near the supported text. Mark unresearched areas and access failures. Do not bury contradictions in a generic caveats section.

## Verdict rules

- `Reject`: a fatal gate or disproportionate downside is evidenced and no cheap reframe is plausible.
- `Reframe`: the current segment, route, payer, problem framing, or risk model fails, but a materially different testable hypothesis is supported.
- `Validate`: the opportunity survives screening but the decision bottleneck still requires behavior evidence.
- `Evidence-supported`: evidence appropriate to the present decision exists; this still does not guarantee profit.

Build boundary:

- `Closed`: no implementation beyond research artifacts.
- `Limited evidence-bearing slice`: only the named prototype/manual workflow/instrument needed for the experiment.
- `Open for specified scope`: only the scope justified by accumulated evidence; broader roadmap remains unapproved.

## Compactness rules

- Do not repeat the same evidence in narrative, table, and appendix.
- Prefer ranges and explicit unknowns to false precision.
- Cite methodology only when requested; cite current market evidence always when material.
- Stop after one decisive next action. Offer deeper evidence records only if useful.
- Never claim the skill guarantees revenue, certainty, product-market fit, or legal compliance.

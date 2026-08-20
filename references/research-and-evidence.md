# Research and evidence discipline

Use this whenever current external facts influence the decision. The goal is traceability, not a long bibliography.

## Claim–evidence ledger

Assign stable IDs: `C1` for claims and `E1` for evidence. Never reuse an ID for a changed statement.

### Claim record

```yaml
id: C1
statement: Specific falsifiable statement
status: Fact | Inference | Hypothesis | Unknown
importance: fatal | ranking | context
evidence_ids: [E1]
contradicts: [E2]
limitations: What this claim does not establish
```

### Evidence record

```yaml
id: E1
title: Source or experiment title
url: https://example.com/page
publisher: Publisher or platform
published_or_updated: YYYY-MM-DD | unknown
retrieved: YYYY-MM-DD
observed_event_date: YYYY-MM-DD | unknown
segment: Relevant actors
geography: Relevant market
provenance: public-source | user-report | experiment-result
evidence_type: policy | price | review | interview | observed-behavior | payment | other
direction: supports | contradicts | mixed
origin_id: ORIGIN-1
fitness: Why this source can support this exact claim
limitations: Coverage, bias, sample, ambiguity, or access limit
```

For a user report without a URL, do not label the claim `Fact` as if independently verified. Preserve provenance and state whether it is accepted as task context or still material to verify.

## Status rules

- `Fact`: directly supported by cited evidence for the narrow statement made.
- `Inference`: a disclosed conclusion drawn from facts; cite its inputs.
- `Hypothesis`: a claim that can be tested but is not established.
- `Unknown`: material information not yet established, including source-access failure.

Do not promote an inference because multiple articles repeat it. Do not turn “not found” into “does not exist” unless search coverage and the justified scope of that negative claim are explicit.

## Source fitness and independence

Judge fitness per claim:

- first-party policy is strong for the policy, weak for demand;
- a current official price page is strong for listed price, not customer value;
- a buyer's recent paid workaround is strong for that buyer's behavior, not total market size;
- reviews are useful for recurring circumstances and alternatives, but selection-biased;
- search trends are normalized samples and indicate attention, not willingness to pay;
- a founder story is an example, not a base rate.

Track the original source family with `origin_id`. Syndicated articles, reposted announcements, and summaries of one study are one origin, not independent corroboration. Prefer different methods and actors when triangulating.

## Research procedure

1. Write the decision question and the few claims that can change it.
2. Choose source types fitted to each claim.
3. Search the strongest favorable and contrary explanations.
4. Open the source and record exact relevance, dates, segment, geography, and limitations.
5. Deduplicate by original source.
6. Update the claim status without erasing contradictions.
7. Stop when the decision is stable or a live test has higher information value.

For current policy, law, product capability, technical API, price, or fee claims, use a current primary source when available. For high-stakes legal, medical, financial, investment, tax, or regulated issues, state that research is not professional advice, do not infer compliance or suitability, and seek applicable jurisdictional authority or qualified advice.

## Failure and freshness

- Record paywalls, robots blocks, deleted pages, search failures, and ambiguous dates as limitations or unknowns.
- Never silently replace live research with model memory.
- Recheck mutable claims close to the experiment or build decision.
- Use observed event date separately from article publication date when timing matters.
- State which markets, languages, and surfaces were not researched.

## Bias controls

- **Confirmation bias:** search for sufficient-free-alternative and no-budget explanations.
- **Survivorship bias:** do not infer likelihood from visible winners; seek abandoned or pivoted attempts when relevant.
- **Selection bias:** reviews and community posts overrepresent some users and outcomes.
- **Hypothetical bias:** “I would buy” generally overstates real commitment; do not convert it to revenue.
- **False precision:** ranges and explicit unknowns are preferable to invented probabilities.

## Evidence ladder

Use the ladder in `SKILL.md` only as a guide to behavioral commitment. Strength remains claim-specific. A deposit can support willingness to pay for one offer, but not retention or scalable acquisition. Multiple interviews can establish recurring circumstances but not transaction behavior.

## Packet linting

When a structured JSON research packet exists, run `scripts/validate_packet.py`. It also checks that every opportunity has an explicitly evidenced, conditional, or unknown first-customer route consistent with its fatal gate. Fix structural errors, then review semantic truth manually. The linter cannot determine whether a source is honest, current enough, or interpreted correctly.

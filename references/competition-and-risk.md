# Competition, dead zones, and risk

Use this before scoring an opportunity and whenever new evidence can change a fatal gate.

## Alternatives map

Compare the user's intended outcome against:

1. direct specialist products;
2. adjacent or bundled products;
3. generic tools and automation platforms;
4. spreadsheets, documents, scripts, and manual work;
5. employee, contractor, agency, or outsourced service;
6. postponing or doing nothing.

For each relevant alternative record price or cost range, target segment, sufficient outcome, switching/migration burden, learning/habit, integration/data lock-in, trust, support, and the trigger that might cause a switch. Feature gaps are not opportunities unless the reachable segment cares enough to change behavior.

## Free-alternative gate

Ask:

- Is the free/current option sufficient in the target circumstance?
- Which consequence makes its limitation costly now?
- Who bears that cost and controls budget?
- What must be migrated, relearned, trusted, or approved?
- Is the proposed advantage large enough to justify those switching costs?

If no concrete switching trigger exists, keep willingness to switch as `Unknown`; do not treat dissatisfaction as intent to replace.

## Opportunity versus dead zone

For every apparent gap, write two competing explanations:

- **Opportunity reading:** a reachable segment has an important unresolved job and current alternatives are inadequate.
- **Dead-zone reading:** low payment, rare frequency, high acquisition/support cost, trust, regulation, data access, platform limits, or adequate free workarounds make the gap uneconomic.

Seek evidence for both. Review failed, abandoned, or pivoted entrants when reliably documented. Low competitor count is never automatically positive.

## Risk topology

Cover only material risks, but consider:

- acquisition and sales-cycle dependence;
- switching, onboarding, and migration burden;
- founder identity, reputation, security, and buyer trust;
- platform/API/payment dependency and policy change;
- data availability, consent, privacy, retention, and security;
- jurisdiction, license, regulated advice, consumer protection, refunds, tax, and claims;
- technical dependency concentration and service reliability;
- delivery, moderation, support, abuse, and manual-operations load;
- unit-economics range including founder time, fees, infrastructure, support, churn, and refunds;
- downside, reversibility, and blast radius.

Classify each material risk:

- `Kill now`: cannot be accepted or economically mitigated.
- `Mitigate before experiment`: a safeguard or policy check is required first.
- `Watch`: define a trigger and review point.
- `Accept`: explain why residual downside is proportionate.

Every mutable platform or regulatory claim needs a current primary source. Separate legal research from legal advice.

## Required-data access

For every third-party or device-data dependency, classify the proposed path:

1. documented public API;
2. approved restricted program;
3. user-initiated export or share;
4. privileged local permission;
5. scraping, reverse engineering, or unauthorized automation.

Record whose consent is required, whether non-user data is included, distribution constraints, and a current primary source. Treat category 5 as a kill gate. Category 4 grants a technical capability, not platform authorization, third-party consent, or legal permission.

## Risk record

```yaml
id: R1
risk: Specific event or constraint
category: platform | legal | privacy | security | economic | trust | operational | technical
status: kill | mitigate | watch | accept
likelihood: low | medium | high | unknown
impact: low | medium | high | unknown
evidence_ids: [E1]
mitigation: Concrete action or none
trigger: Observable condition for reevaluation
residual_unknown: What remains uncertain
```

Do not multiply guessed likelihood and impact into a precise expected-loss number. Use the record to decide gates, experiment safeguards, and the allowed build boundary.

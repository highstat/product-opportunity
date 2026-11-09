# product-opportunity

> Find evidence-backed software opportunities, compare their risks, and design a cheap demand test before writing code.

`product-opportunity` is an open-source Codex skill for developers, solo builders, product people, and small teams deciding what software is worth testing. It starts with buyers you can actually reach, looks for observable problem signals and current alternatives, and recommends the cheapest useful next experiment before product development.

It is especially useful when you have a rough app idea, several ideas to compare, or no idea yet but a limited budget and no existing audience.

## Try it now

Paste this into a Codex task:

```text
Use $skill-installer to install product-opportunity from repository
https://github.com/highstat/product-opportunity, using path . and the name
product-opportunity.
```

Then open a new task and copy the prompt in [Quick start](#quick-start).

## Why this exists

Developers often start with an idea and code, then discover that they cannot reach buyers, the problem is not urgent, a free alternative is already good enough, or stated interest does not turn into payment.

This skill reverses that sequence:

1. identify a reachable segment and a permitted path to potential buyers;
2. examine recurring problems, current behavior, competitors, and workarounds;
3. separate verified facts from inferences, hypotheses, and unknowns;
4. eliminate opportunities blocked by distribution, economics, access, trust, legal, platform, privacy, or ethical risk;
5. run one cheap experiment that can change the decision;
6. decide whether to `validate`, `revise`, or `stop` before committing to a build.

## What it does

- Finds buyer segments the user can plausibly reach.
- Collects current signals of recurring, consequential problems.
- Analyzes direct competitors, free tools, manual work, services, and doing nothing.
- Compares surviving opportunities with goal-dependent weights and sensitivity checks.
- Designs low-cost demand experiments with precommitted success, failure, and inconclusive outcomes.
- Preserves evidence from previous experiments and updates only the assumptions actually tested.
- Produces a compact decision card instead of a generic startup report.

## What it does not do

- It does not guarantee profit, product-market fit, customers, or commercial success.
- It is not financial, investment, legal, tax, or other professional advice.
- It does not treat likes, search volume, waitlists, or verbal enthusiasm as proof of willingness to pay.
- It does not automatically start product development.
- It does not contact people, publish content, buy tools, collect payments, register services, or perform other external actions without the user's explicit authorization.
- It does not recommend spam, deception, prohibited scraping, covert data collection, or platform-rule evasion.

## Install

In a Codex task, paste this single instruction:

```text
Use $skill-installer to install the skill from repository
https://github.com/sprensis/product-opportunity, using path . and the name
product-opportunity.
```

Restart Codex or open a new task after installation so the skill catalog refreshes.

<details>
<summary>Manual installation</summary>

Requires Git, `rsync`, and a Codex installation. Run the following from a directory where you want to clone the repository:

```bash
git clone https://github.com/sprensis/product-opportunity.git
cd product-opportunity
test -f SKILL.md && mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills/product-opportunity" && rsync -a --delete --delete-excluded --exclude '.git/' --exclude '.DS_Store' --exclude '__pycache__/' --exclude '*.pyc' ./ "${CODEX_HOME:-$HOME/.codex}/skills/product-opportunity/"
```

The `--delete` option makes the installed copy match the repository. Keep personal modifications in a fork or commit them before updating.

</details>

## Quick start

Copy this into a Codex task after installation:

```text
Use $product-opportunity in discover mode.

Find a small software opportunity that could help a beginner developer test a path
to their first $100. I have no audience and little marketing experience, so start
with a reachable distribution channel. Do not recommend building until you examine
competitors, recurring user complaints, and a cheap way to test willingness to pay.
```

The skill may ask up to five decision-relevant questions at a time, research current public sources, reject weak candidates, and return fewer than three opportunities when the evidence does not support a longer list.

## Modes

| Mode | Use it when | Expected decision |
|---|---|---|
| `discover` | You do not yet have a validated idea | Find evidence-supported opportunities from reachable channels, or report that no candidate survives |
| `evaluate` | You already have one idea | Decide whether to reject, reframe, or validate it |
| `compare` | You have several possible ideas | Compare only gate-passing candidates under your actual goal and constraints |
| `validate` | One assumption is blocking a decision | Design one cheapest adequate experiment with measurable outcomes |
| `review-results` | You completed an experiment | Classify the result, preserve negative evidence, and decide to continue, revise, rerun, or stop |

## Example prompts

### Evaluate an attractive but unproven idea

```text
Use $product-opportunity in evaluate mode for a macOS menu-bar app that automatically
organizes screenshots. Check current built-in and free alternatives, identify a
permitted route to the first buyers, and keep the build boundary closed until a
behavioral demand test passes.
```

### Compare three ideas for a solo developer

```text
Use $product-opportunity in compare mode. Compare these ideas for a solo developer
with $100, four weeks, simple backend skills, and no paid audience: [idea A], [idea B],
and [idea C]. Derive the weights from my goal, apply fatal gates before scoring, and
show whether the ranking is robust or fragile.
```

### Design a B2B validation test

```text
Use $product-opportunity in validate mode. I can speak with independent dental-clinic
managers, but promotional posts require admin approval. My riskiest assumption is
that managers will pay to reduce a recurring reconciliation task. Choose the cheapest
permitted experiment that can test payment behavior without building the software.
```

### Review an inconclusive result

```text
Use $product-opportunity in review-results mode. The offer received no replies, but
the sending domain was placed in spam and only two qualified prospects saw it.
Compare the result with the precommitted criteria, preserve prior evidence, and decide
whether the hypothesis failed or the test was invalid.
```

### Find a low-maintenance opportunity

```text
Use $product-opportunity in discover mode. I want a small, low-maintenance software
product for English-speaking freelancers. I have ten hours per week and can reach
people only through communities that allow research but restrict promotion. Prioritize
permitted first-customer paths, support burden, and reversibility over market size.
```

## Illustrative end-to-end example

> **Illustrative only:** every signal, score, threshold, and outcome below is synthetic. This is a demonstration of the workflow, not completed market research, customer interviews, sales evidence, or a claim that these opportunities are attractive today.

### Starting situation

A beginner frontend developer has no audience, a `$40` test budget, two weeks, and a goal of testing a path toward a first `$100`. The only assumed acquisition surface in this example is a public freelance marketplace where buyers post tasks and qualified replies are permitted.

### Synthetic input signals

- Some hypothetical buyer posts describe cleaning malformed CSV exports before store migrations.
- The hypothetical buyers currently repair files manually or pay for one-off spreadsheet work.
- General PDF utilities appear easy to build, but operating-system and browser tools already cover much of the workflow for free.
- AI content generators receive attention in broad communities, but the example contains no payment evidence and no permitted narrow route to a buyer.

These are assumptions supplied to demonstrate the process. In a real run, the skill would need current opened sources, retrieval dates, source limitations, and a clear separation between `Fact`, `Inference`, `Hypothesis`, and `Unknown`.

### Three compared opportunities

| Opportunity | First-customer route | Main evidence gap | Decision |
|---|---|---|---|
| Manually clean store-migration CSV files, then automate repeated steps | Reply only to qualifying buyer-posted jobs on a marketplace that permits proposals | Whether buyers will pay this developer for the scoped outcome and whether the work recurs | `validate` with a paid manual service |
| Build a general PDF merge/compress/sign app | Search traffic, with no direct buyer relationship in the example | A switching trigger strong enough to beat sufficient free alternatives | `stop` for the current framing |
| Build a general AI social-content generator | Broad communities where promotion may be restricted | Reachable payer, differentiated workflow, and consequential commitment | `revise` or reject until a narrower segment and route are evidenced |

The PDF utility is rejected because an easy implementation and visible search interest do not overcome sufficient free alternatives and weak distribution. The content generator is rejected because broad interest is not a first-customer path. The CSV workflow survives only as a testable service hypothesis—not as permission to build a full product.

### Cheapest adequate experiment

```yaml
hypothesis: A qualified buyer with an active store-migration task will pay for a narrowly scoped, manually delivered CSV cleanup.
segment: Buyer-posted jobs that explicitly mention malformed catalog or migration data.
channel: Permitted replies to relevant public marketplace requests; no unsolicited bulk messages.
instrument: Paid manual service delivered without product code.
denominator: 10 qualifying requests, if that many occur during the timebox.
max_cash: $0
founder_time: 3 hours
timebox: 7 days
success: At least one buyer pays for the scoped service; keep the full build closed and next test recurrence and delivery economics.
failure: No buyer advances after 10 valid, visible, qualified replies; revise the offer or segment, or stop.
inconclusive: Fewer than 10 qualifying requests appear, replies are not visible, or platform rules prevent the test; do not interpret this as no demand.
```

The number `10` is an illustrative exposure limit, not a universal conversion benchmark. A real threshold must follow the user's economics, channel, downside, and attainable exposure.

## Repository structure

```text
product-opportunity/
├── SKILL.md                    # Compact routing and non-negotiable rules
├── agents/openai.yaml          # Codex UI metadata and invocation policy
├── references/                 # Mode-specific research and decision guidance
├── scripts/                    # Standard-library-only deterministic helpers
├── tests/                      # Unit tests and behavioral acceptance scenarios
├── CONTRIBUTING.md             # Useful feedback and contribution guidance
├── LICENSE                     # MIT License
└── README.md
```

The skill uses progressive disclosure: `SKILL.md` contains shared rules and routes each mode only to the references it needs. The methodology bibliography is not loaded as evidence for a user's current market.

## Methodology and sources

The workflow synthesizes customer discovery, Jobs to Be Done, evidence-led user research, first-customer sales, lean experiments, multi-criteria decision analysis, and risk screening. It uses these methods as testable decision tools, not as proof that a product will succeed.

Key implementation references:

- [`references/research-and-evidence.md`](references/research-and-evidence.md) — claim–evidence records, source fitness, provenance, freshness, and bias controls.
- [`references/first-customer-path.md`](references/first-customer-path.md) — a traceable route from buyer trigger to permitted ask.
- [`references/competition-and-risk.md`](references/competition-and-risk.md) — alternatives, dead-zone explanations, access, legal, privacy, platform, and economic gates.
- [`references/scoring-model.md`](references/scoring-model.md) — objective-dependent weights, ranges, confidence, and sensitivity.
- [`references/validation-experiments.md`](references/validation-experiments.md) — cheapest adequate experiment selection.
- [`references/experiment-learning.md`](references/experiment-learning.md) — append-only learning from supported, weakened, falsified, inconclusive, and invalid tests.
- [`references/sources.md`](references/sources.md) — source attribution, access dates, exact uses, and limitations.

## Validation

The helper scripts require Python 3.9 or later and use only the Python standard library.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -B "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

The unit tests verify deterministic mechanics. `quick_validate.py` checks the Codex package shape and frontmatter. Neither proves that a market source is truthful or that a human judgment is correct.

## Limitations

- The skill reduces uncertainty; it cannot guarantee revenue, product-market fit, or legal compliance.
- It is not financial, investment, legal, tax, or other professional advice.
- Market, price, competitor, legal, and platform claims can change and must be rechecked near the decision.
- Early tests may fail because of segment, message, recruitment, channel, instrumentation, or delivery—not only because the problem is absent.
- A paid pilot supports a narrow offer and segment; it does not prove retention or scalable acquisition.
- Legal, privacy, security, tax, or regulated-domain decisions may require qualified advice in the applicable jurisdiction.
- Research and experiment plans do not authorize external actions.

## Contributing

Installation reports, evidence-quality failures, unsafe recommendations, unclear decisions, and focused improvements are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before opening an issue or pull request. Do not include secrets, private customer information, or confidential research data.

## License

MIT License. Copyright © 2026 [highstat](https://github.com/highstat/). See [`LICENSE`](LICENSE).

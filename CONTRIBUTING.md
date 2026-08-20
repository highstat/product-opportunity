# Contributing

Thanks for helping improve `product-opportunity`. The most useful contributions make the skill safer, more evidence-disciplined, easier to install, or more decisive without adding unsupported certainty.

## Useful feedback

When opening an issue, describe the smallest reproducible case and tell us:

- whether installation was clear and which Codex environment you used;
- which mode you invoked: `discover`, `evaluate`, `compare`, `validate`, or `review-results`;
- whether the result separated facts, inferences, hypotheses, and unknowns;
- whether it found a permitted path to first customers instead of naming a broad channel;
- whether it rejected a weak idea when evidence or a fatal gate required that;
- whether the proposed experiment was cheaper than building and had success, failure, and inconclusive outcomes;
- which part of the output was unclear, too verbose, or not actionable.

Redacted excerpts are welcome. Never post API keys, tokens, passwords, private customer data, confidential research, paid source material, or identifying interview notes.

## Reporting unsafe behavior

Please report recommendations involving spam, deception, prohibited scraping, covert data collection, financial promises, policy evasion, or unapproved external actions. If the report contains a real secret or exploitable private detail, do not put it in a public issue. Use GitHub's private vulnerability-reporting flow if it is available; otherwise open a minimal issue asking the maintainer for a private contact without including the sensitive content.

## Pull requests

Keep changes focused and explain the observed failure they address. Avoid adding universal thresholds, generic startup advice, duplicated checklists, mandatory paid tools, or large copied excerpts from external sources.

Before submitting a pull request, run:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -B "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-creator/scripts/quick_validate.py" .
```

Add or update a behavioral scenario when a change affects decisions rather than wording. Do not write tests that merely match a heading or a preferred prose style.

By submitting a contribution, you agree that it may be distributed under the repository's MIT License.

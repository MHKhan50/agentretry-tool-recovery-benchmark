# Dataset Card: AgentRetry Synthetic Tool-Recovery Scenarios

## Summary
`data/scenarios.csv` is a synthetic, generated scenario set used to compare four deterministic recovery policies. It contains no personal data, scraped content, or external dataset records.

## Intended uses
- Teaching and dissertation exercises about agent reliability, tool semantics, retry logic, and reproducibility.
- Baseline policy comparisons under explicitly stated assumptions.
- Testing metric pipelines and scenario generators before running costly experiments.

## Out-of-scope uses
- Claiming production safety, commercial-agent performance, or real-world incident rates.
- Making safety-critical decisions.
- Treating the generated distribution as representative of real tool failures.

## Fields
- `scenario_id`: stable scenario identifier for the default seed.
- `operation_type`: `read`, `idempotent_write`, or `non_idempotent_action`.
- `failure_mode`: `no_failure`, `pre_execution_failure`, `post_execution_timeout`, or `stale_observation`.
- `ledger_available`: whether the simulated operation ledger can confirm the result.
- `seed`: random seed used to generate the dataset.

## Generation and provenance
Generated locally by `generate_dataset.py` with Python's standard-library `random.Random`. Default run: 800 scenarios, seed `20261029`. The data can be regenerated with `python3 run_benchmark.py --n 800 --seed 20261029`. Because this is synthetic data, there are no third-party dataset attribution obligations. The scenario assumptions are documented in `README.md`.

## Known limitations
The model assumes a single critical operation per episode, transient pre-execution failures, immediate side effects for post-execution timeouts, and a simplified ledger. The generator uses fixed scenario weights. These choices can bias results and should be varied in sensitivity analysis.

## Licence
Dataset and generated outputs: Creative Commons Attribution 4.0 International (CC BY 4.0). Code: MIT License. Attribution is requested when reusing the dataset or graph.

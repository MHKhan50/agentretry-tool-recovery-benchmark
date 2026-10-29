# AgentRetry: A Synthetic Benchmark for Recovering from Ambiguous Tool Outcomes

**Version:** 0.1.0
**Author:** Muzammal Hussain
**Date:** 29 October 2026
**Runtime:** Python 3.9.6+; standard library only

## Research question

When an agent's tool call fails before execution, times out after a side effect has occurred, or returns a stale observation, how do simple recovery policies trade task completion against duplicate side effects?

This is a **synthetic, mechanism-focused benchmark**. It is not a test of a live LLM, production software, or real users. Its purpose is to make recovery assumptions explicit and reproducible before testing them against real tools.

## Why this is useful

A multi-step agent can receive an error even when a requested action has already happened. Blind retries may repeat a non-idempotent action (for example, sending a notification or creating a second ticket). Refusing every uncertain action can avoid duplication but leave tasks unfinished. This benchmark compares four transparent policies under the same generated scenarios.

The topic is motivated by current UK university research interest in evaluating agentic AI in software/data engineering and in long-horizon task execution with error recovery. See `research_context.md`; these sources are context, not endorsements or evidence that this benchmark is novel.

## Quick start (Mac)

From this project folder:

```bash
python3 run_benchmark.py
```

Run the unit tests:

```bash
python3 -m unittest discover -s tests -v
```

Regenerate a larger dataset with a chosen seed:

```bash
python3 run_benchmark.py --n 2000 --seed 20261029
```

No network access, model download, API key, GPU, or third-party package is required. Python 3.9.6 is sufficient. Ollama/Qwen/Llama are not needed for the core experiment; they could be added later as policy-decision adapters, but such an extension would be a separate experiment.

## Policies compared

- `blind_retry`: retries after every simulated failure, including ambiguous outcomes.
- `bounded_retry`: retries only when the first call failed before execution; escalates ambiguous outcomes.
- `verify_then_act`: checks a simulated operation ledger after ambiguous outcomes; completes only when verification is available, otherwise escalates.
- `stop_and_escalate`: stops after any failure rather than retrying.

These are deliberately simple reference policies, not claims about any commercial agent framework.

## Scenario design

Each generated episode represents a critical tool operation inside a larger workflow. The scenario varies:

- operation semantics: read, idempotent write, or non-idempotent action;
- outcome: no failure, pre-execution failure, post-execution timeout, or stale observation;
- whether an operation ledger is available for verification.

A post-execution timeout and stale observation mean the first operation's side effect has occurred, although the agent does not have a trustworthy result. A pre-execution failure means no effect occurred. A retry succeeds in the simplified model. Those assumptions are intentional and must be stress-tested before generalising.

## Outputs

Running the benchmark creates/refreshes:

- `data/scenarios.csv` — generated synthetic scenarios;
- `outputs/episode_results.csv` — one row per scenario-policy pair;
- `outputs/summary.csv` and `outputs/summary.json` — aggregate metrics;
- `outputs/completion_vs_duplicate_risk.svg` — dependency-free SVG graph.

Key metrics:

- **completion rate:** fraction of episodes the policy reports complete;
- **safe completion rate:** reported completion without a simulated duplicate non-idempotent side effect;
- **duplicate side-effect rate on ambiguous non-idempotent cases:** duplicates divided by the number of cases where a non-idempotent operation had a post-execution timeout or stale observation;
- **escalation rate:** fraction sent for human/manual follow-up;
- **mean tool calls:** average calls, including verification calls;
- **failure recovery rate:** completion rate among episodes with a simulated failure.

The denominator for duplicate risk is restricted to ambiguous non-idempotent cases; the summary includes that denominator explicitly. Always report both rates and counts.

## Interpretation cautions

1. Results are conditional on the simulator's assumptions and chosen scenario distribution.
2. The benchmark uses one critical operation per episode to isolate recovery behaviour; it does not model a complete multi-step agent or realistic tool latency.
3. Retries are assumed to succeed after a pre-execution failure. Real failures can be persistent.
4. The simulated ledger is a simplified oracle; real verification may be incomplete, delayed, costly, or wrong.
5. No statistical confidence intervals are included in this baseline. For a paper, add repeated seeds, uncertainty intervals, sensitivity analyses, and an independently reviewed scenario model.
6. Do not describe these synthetic results as evidence of production safety or real-LLM performance.

## Reproducibility and extension

- The scenario generator is deterministic for a given seed.
- Core code and tests use the Python standard library only.
- To extend: add persistent-failure cases, delayed side effects, partial commits, idempotency keys, multi-step dependencies, and alternative verification costs. Preserve the baseline and report all changed assumptions.
- A future LLM adapter should log model/version, prompt, decoding settings, tool schemas, hardware, and failures. Do not mix adapter results with the current synthetic baseline.

## Citation and licence

Code: MIT License (`LICENSE`).
Synthetic dataset and generated outputs: CC BY 4.0 (`dataset_card.md`).
Citation metadata: `CITATION.cff`.

See `PUBLICATION_CHECKLIST.md` before uploading to GitHub, Kaggle, a website, or a DOI repository.

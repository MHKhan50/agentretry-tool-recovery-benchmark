# AgentRetry: Benchmarking Recovery Policies for Ambiguous Tool Outcomes in Agentic Workflows

**Author:** Muzammal Hussain
**Status:** Synthetic benchmark preprint draft; not peer-reviewed
**Date:** 29 October 2026

## Abstract

Tool-using agents can receive a timeout or stale observation after an operation has already changed state. Retrying without checking the operation's outcome can duplicate non-idempotent side effects, while stopping on every failure can reduce task completion. This work introduces AgentRetry, a lightweight synthetic benchmark that compares four transparent recovery policies under pre-execution failures, post-execution timeouts, and stale observations. Scenarios vary operation semantics and the availability of a simulated operation ledger. The benchmark reports task completion, safe completion, duplicate-side-effect risk, escalation, tool-call count, and recovery on failure. The baseline is designed to be reproducible with Python's standard library and is not a measurement of a live language model or production system.

## Research question

How do simple recovery policies trade completion against duplicate side effects when a tool outcome is ambiguous?

## Motivation and relation to current UK research

The University of Glasgow announced an empirical research partnership in March 2026 to study how agentic AI affects software and data engineering, including efficacy and workflow impact. The University of Leeds' current long-horizon robotics PhD project identifies planning, disturbances, and error recovery in multi-stage tool-use tasks as research challenges. These examples show relevant research activity; they do not establish that the present benchmark is novel or endorsed by either institution.

## Method

The generator creates synthetic scenarios with three operation classes and four outcome classes. Four deterministic reference policies are evaluated against the same scenarios: blind retry, bounded retry, verify-then-act, and stop-and-escalate. The simulator treats a pre-execution failure as having no side effect; a post-execution timeout or stale observation as an operation whose side effect has already occurred; and a retry after a pre-execution failure as successful. The verification policy succeeds only when the simulated ledger is available. These are modelling assumptions, not empirical facts about deployed systems.

## Baseline results

The included default run uses 800 scenarios and seed `20261029`, yielding 3,200 scenario-policy episodes. Its aggregate results are shown below and are reproducible with `python3 run_benchmark.py`. The values describe only this synthetic configuration; they are not live-agent measurements.

| Policy | Completion | Safe completion | Duplicate risk* | Escalation | Mean tool calls |
|---|---:|---:|---:|---:|---:|
| blind_retry | 1.000 | 0.864 | 1.000 | 0.000 | 1.587 |
| bounded_retry | 0.654 | 0.654 | 0.000 | 0.346 | 1.241 |
| verify_then_act | 0.909 | 0.909 | 0.000 | 0.091 | 1.587 |
| stop_and_escalate | 0.412 | 0.412 | 0.000 | 0.588 | 1.000 |

*Duplicate risk is measured only among ambiguous non-idempotent cases. See `outputs/summary.csv` for the denominator and duplicate count. These point estimates do not include confidence intervals.

## Limitations

The baseline has one critical operation per episode, fixed scenario weights, transient failures, and an idealised verification ledger. It does not model persistent faults, concurrent operations, partial commits, latency distributions, realistic API semantics, or model-generated decisions. The benchmark currently reports point estimates only. A stronger study should vary seeds and scenario weights, report confidence intervals, include persistent and delayed failures, compare alternative ledger reliability/cost, and evaluate on a carefully documented real-tool testbed.

## Reproducibility

The project uses Python 3.9.6+ and the standard library only. Run the benchmark with `python3 run_benchmark.py` and tests with `python3 -m unittest discover -s tests -v`. Scenario data are synthetic and reproducible from the supplied generator and seed.

## Conclusion

AgentRetry provides a small, inspectable baseline for studying an important design trade-off: retrying may improve apparent completion but can create duplicate non-idempotent effects; verification can reduce this risk when reliable evidence is available; and escalation trades autonomy for caution. The findings should be treated as hypotheses for subsequent evaluation, not evidence that one policy is universally best.

## References

1. University of Glasgow. (30 March 2026). *UofG and Lloyds Banking Group announce agentic AI research programme.* https://www.gla.ac.uk/news/headline_1256583_en.html
2. University of Leeds. *Long-Horizon Robotic Dexterous Manipulation* (PhD project page; project start date listed as 1 October 2026). https://phd.leeds.ac.uk/project/2300-long-horizon-robotic-dexterous-manipulation

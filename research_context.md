# Research Context and Topic Selection — 29 October 2026

## Topic selected
**AgentRetry: recovery policies for ambiguous tool outcomes in agentic workflows.**

The question is deliberately narrower than general agent safety: when a tool reports failure but the action may already have taken effect, how should an agent balance completion, verification, duplicate side effects, and escalation?

## Official UK university evidence checked on 29 October 2026

1. **University of Glasgow — agentic AI in software and data engineering.** Its 30 March 2026 announcement describes a four-year partnership that will empirically study agentic AI in software/data engineering, with experiments on efficacy and measurement of efficiency/workflow impact. This supports the relevance of reproducible evaluation of agents in engineering workflows; it does not prove a specific retry-policy gap.
   https://www.gla.ac.uk/news/headline_1256583_en.html

2. **University of Leeds — long-horizon robotic dexterous manipulation.** The official PhD page lists a project start date of 1 October 2026 and identifies long-horizon task decomposition, disturbances, error recovery, and benchmark datasets as challenges. This is adjacent evidence for the general importance of recovery and reproducible evaluation in sequential tool-use systems; the project is robotics-focused, not this benchmark.
   https://phd.leeds.ac.uk/project/2300-long-horizon-robotic-dexterous-manipulation

3. **University of Southampton — secure and trustworthy AI for autonomous vehicle ecosystems.** The official postgraduate research page describes work on threat modelling, resilience, and mitigation in AI-enabled autonomous systems and lists a 30 November 2026 closing date on the page when checked. This is broader adjacent evidence for resilient AI systems; it is not a direct match to the synthetic tool-retry experiment.
   https://www.southampton.ac.uk/study/postgraduate-research/projects/secure-trustworthy-ai-for-autonomous-vehicle-ecosystems

## Evidence vs. inference
- **Observed evidence:** official UK university pages describe current research in empirical evaluation of agentic AI, error recovery in long-horizon tasks, and trustworthy/resilient AI systems.
- **Research inference:** a small, reproducible benchmark can help students operationalise and stress-test recovery assumptions before implementing a live-tool experiment.
- **Not claimed:** that this is the hottest topic, that no prior work exists, that the benchmark is institutionally endorsed, or that this synthetic experiment proves production-agent safety.

## Research-gap statement (provisional)
A useful, defensible student research question is whether explicit verification of ambiguous tool outcomes improves the completion-versus-duplicate-side-effect trade-off under different failure distributions and verification reliability. This package provides a baseline mechanism model, not a literature review sufficient to establish novelty. Before submitting a dissertation or paper, search recent peer-reviewed work on distributed systems' exactly-once semantics, idempotency, LLM tool-use reliability, agent benchmarks, and fault recovery, and position the contribution against that literature.

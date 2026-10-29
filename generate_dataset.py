"""Generate deterministic, fully synthetic AgentRetry scenarios."""
from __future__ import annotations

import argparse
import csv
import random
from pathlib import Path

OPERATIONS = ("read", "idempotent_write", "non_idempotent_action")
FAILURES = ("no_failure", "pre_execution_failure", "post_execution_timeout", "stale_observation")
FIELDS = ("scenario_id", "operation_type", "failure_mode", "ledger_available", "seed")


def generate_scenarios(n: int = 800, seed: int = 20261029) -> list[dict]:
    if n < 1:
        raise ValueError("n must be at least 1")
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        operation = rng.choices(OPERATIONS, weights=(0.25, 0.35, 0.40), k=1)[0]
        failure = rng.choices(FAILURES, weights=(0.42, 0.22, 0.22, 0.14), k=1)[0]
        ledger = int(rng.random() < 0.72)
        rows.append({
            "scenario_id": "AR-20261029-%05d" % i,
            "operation_type": operation,
            "failure_mode": failure,
            "ledger_available": ledger,
            "seed": seed,
        })
    return rows


def write_scenarios(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=800)
    parser.add_argument("--seed", type=int, default=20261029)
    parser.add_argument("--output", default="data/scenarios.csv")
    args = parser.parse_args()
    rows = generate_scenarios(args.n, args.seed)
    write_scenarios(rows, Path(args.output))
    print("Generated %d synthetic scenarios at %s (seed=%d)" % (len(rows), args.output, args.seed))


if __name__ == "__main__":
    main()

"""Run the complete AgentRetry baseline from generation through graph output."""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

from benchmark import evaluate, write_outputs
from generate_dataset import generate_scenarios, write_scenarios
from plot_results import plot_results


def read_scenarios(path: Path) -> list[dict]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["ledger_available"] = int(row["ledger_available"])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the AgentRetry synthetic benchmark.")
    parser.add_argument("--n", type=int, default=800, help="number of synthetic scenarios")
    parser.add_argument("--seed", type=int, default=20261029, help="random seed")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    data_path = root / "data" / "scenarios.csv"
    output_dir = root / "outputs"
    scenarios = generate_scenarios(args.n, args.seed)
    write_scenarios(scenarios, data_path)
    rows, summaries = evaluate(scenarios)
    write_outputs(rows, summaries, output_dir)
    plot_results(output_dir / "summary.csv", output_dir / "completion_vs_duplicate_risk.svg")

    print("AgentRetry synthetic baseline complete")
    print("Scenarios: %d | policy episodes: %d | seed: %d" % (len(scenarios), len(rows), args.seed))
    print("Policy summary:")
    for item in summaries:
        print(
            "  {policy:18s} completion={completion_rate:.3f} safe={safe_completion_rate:.3f} "
            "duplicate-risk={duplicate_side_effect_rate_on_ambiguous_non_idempotent:.3f} "
            "escalation={escalation_rate:.3f} mean-calls={mean_tool_calls:.3f}".format(**item)
        )
    print("Outputs: outputs/summary.csv, outputs/summary.json, outputs/episode_results.csv")
    print("Graph: outputs/completion_vs_duplicate_risk.svg")


if __name__ == "__main__":
    main()

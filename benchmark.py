"""Policy simulator and metrics for the AgentRetry synthetic benchmark."""
from __future__ import annotations

import csv
import json
from pathlib import Path

POLICIES = ("blind_retry", "bounded_retry", "verify_then_act", "stop_and_escalate")
AMBIGUOUS = {"post_execution_timeout", "stale_observation"}
FAILURES = {"pre_execution_failure", "post_execution_timeout", "stale_observation"}


def simulate_episode(scenario: dict, policy: str) -> dict:
    if policy not in POLICIES:
        raise ValueError("Unknown policy: " + str(policy))

    operation = scenario["operation_type"]
    failure = scenario["failure_mode"]
    ledger = str(scenario["ledger_available"]).lower() in {"1", "true", "yes"}
    non_idempotent = operation == "non_idempotent_action"
    calls = 1
    verification_attempted = 0
    escalated = 0
    completed = 0
    duplicate = 0
    decision = "accept_initial_result"

    if failure == "no_failure":
        completed = 1
        decision = "accept_initial_result"
    elif failure == "pre_execution_failure":
        if policy in {"blind_retry", "bounded_retry", "verify_then_act"}:
            calls += 1
            completed = 1
            decision = "retry_after_pre_execution_failure"
        else:
            escalated = 1
            decision = "escalate_pre_execution_failure"
    elif failure in AMBIGUOUS:
        if policy == "blind_retry":
            calls += 1
            completed = 1
            decision = "blind_retry_after_ambiguous_outcome"
            if non_idempotent:
                duplicate = 1
        elif policy == "verify_then_act":
            calls += 1
            verification_attempted = 1
            if ledger:
                completed = 1
                decision = "verified_effect_already_committed"
            else:
                escalated = 1
                decision = "verification_unavailable_escalate"
        else:
            escalated = 1
            decision = "escalate_ambiguous_outcome"
    else:
        raise ValueError("Unknown failure mode: " + str(failure))

    # A safe completion must be reported complete and must not duplicate a
    # non-idempotent side effect. Other operation types are not penalised here.
    safe_completed = int(bool(completed) and not bool(duplicate))
    return {
        "scenario_id": scenario["scenario_id"],
        "policy": policy,
        "operation_type": operation,
        "failure_mode": failure,
        "ledger_available": int(ledger),
        "task_completed": completed,
        "safe_completed": safe_completed,
        "duplicate_side_effect": duplicate,
        "escalated": escalated,
        "tool_calls": calls,
        "verification_attempted": verification_attempted,
        "decision": decision,
    }


def evaluate(scenarios: list[dict]) -> tuple[list[dict], list[dict]]:
    rows = []
    for scenario in scenarios:
        for policy in POLICIES:
            rows.append(simulate_episode(scenario, policy))

    ambiguous_non_idempotent = sum(
        1 for s in scenarios
        if s["operation_type"] == "non_idempotent_action"
        and s["failure_mode"] in AMBIGUOUS
    )
    summaries = []
    for policy in POLICIES:
        subset = [r for r in rows if r["policy"] == policy]
        n = len(subset)
        failed = [r for r in subset if r["failure_mode"] in FAILURES]
        duplicates = sum(r["duplicate_side_effect"] for r in subset)
        summaries.append({
            "policy": policy,
            "scenario_count": n,
            "completion_rate": round(sum(r["task_completed"] for r in subset) / n, 6) if n else 0.0,
            "safe_completion_rate": round(sum(r["safe_completed"] for r in subset) / n, 6) if n else 0.0,
            "duplicate_side_effect_count": duplicates,
            "ambiguous_non_idempotent_cases": ambiguous_non_idempotent,
            "duplicate_side_effect_rate_on_ambiguous_non_idempotent": round(
                duplicates / ambiguous_non_idempotent, 6
            ) if ambiguous_non_idempotent else 0.0,
            "escalation_rate": round(sum(r["escalated"] for r in subset) / n, 6) if n else 0.0,
            "mean_tool_calls": round(sum(r["tool_calls"] for r in subset) / n, 6) if n else 0.0,
            "failure_recovery_rate": round(
                sum(r["task_completed"] for r in failed) / len(failed), 6
            ) if failed else 0.0,
        })
    return rows, summaries


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_outputs(rows: list[dict], summaries: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_csv(output_dir / "episode_results.csv", rows)
    write_csv(output_dir / "summary.csv", summaries)
    (output_dir / "summary.json").write_text(
        json.dumps({"policies": summaries}, indent=2) + "\n", encoding="utf-8"
    )

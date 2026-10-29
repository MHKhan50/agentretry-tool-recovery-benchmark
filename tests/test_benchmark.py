import csv
import tempfile
import unittest
from pathlib import Path

from benchmark import POLICIES, evaluate, simulate_episode, write_outputs
from generate_dataset import generate_scenarios, write_scenarios


class AgentRetryTests(unittest.TestCase):
    def scenario(self, operation, failure, ledger=1):
        return {
            "scenario_id": "TEST-1",
            "operation_type": operation,
            "failure_mode": failure,
            "ledger_available": ledger,
            "seed": 7,
        }

    def test_generation_is_deterministic(self):
        self.assertEqual(generate_scenarios(20, 7), generate_scenarios(20, 7))

    def test_generator_rejects_zero(self):
        with self.assertRaises(ValueError):
            generate_scenarios(0, 7)

    def test_all_policies_complete_without_failure(self):
        scenario = self.scenario("non_idempotent_action", "no_failure")
        for policy in POLICIES:
            result = simulate_episode(scenario, policy)
            self.assertEqual(result["task_completed"], 1)
            self.assertEqual(result["duplicate_side_effect"], 0)

    def test_blind_retry_can_duplicate_non_idempotent_action(self):
        scenario = self.scenario("non_idempotent_action", "post_execution_timeout")
        result = simulate_episode(scenario, "blind_retry")
        self.assertEqual(result["task_completed"], 1)
        self.assertEqual(result["duplicate_side_effect"], 1)
        self.assertEqual(result["tool_calls"], 2)

    def test_verification_prevents_duplicate_when_ledger_available(self):
        scenario = self.scenario("non_idempotent_action", "post_execution_timeout", 1)
        result = simulate_episode(scenario, "verify_then_act")
        self.assertEqual(result["task_completed"], 1)
        self.assertEqual(result["duplicate_side_effect"], 0)
        self.assertEqual(result["verification_attempted"], 1)

    def test_verification_unavailable_escalates(self):
        scenario = self.scenario("non_idempotent_action", "stale_observation", 0)
        result = simulate_episode(scenario, "verify_then_act")
        self.assertEqual(result["task_completed"], 0)
        self.assertEqual(result["escalated"], 1)

    def test_bounded_retry_recovers_pre_execution_failure(self):
        scenario = self.scenario("idempotent_write", "pre_execution_failure")
        result = simulate_episode(scenario, "bounded_retry")
        self.assertEqual(result["task_completed"], 1)
        self.assertEqual(result["tool_calls"], 2)

    def test_stop_policy_escalates_pre_execution_failure(self):
        scenario = self.scenario("read", "pre_execution_failure")
        result = simulate_episode(scenario, "stop_and_escalate")
        self.assertEqual(result["task_completed"], 0)
        self.assertEqual(result["escalated"], 1)

    def test_outputs_have_four_summary_rows(self):
        scenarios = generate_scenarios(30, 9)
        rows, summaries = evaluate(scenarios)
        self.assertEqual(len(rows), 30 * len(POLICIES))
        self.assertEqual(len(summaries), len(POLICIES))
        with tempfile.TemporaryDirectory() as tmp:
            write_outputs(rows, summaries, Path(tmp))
            with (Path(tmp) / "summary.csv").open(newline="", encoding="utf-8") as handle:
                self.assertEqual(len(list(csv.DictReader(handle))), 4)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations


from pathlib import Path
from unittest.mock import MagicMock

from llm_os_eval.schemas.sample import EvalSample
from llm_os_eval.schemas.result import EvalResult
from llm_os_eval.graders.tool_call import ToolCallEvaluator

SAMPLES_PATH = Path(__file__).parent.parent / "eval" / "internal" / "v0.jsonl"


def _load_samples():
    samples = []
    with open(SAMPLES_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                samples.append(EvalSample.model_validate_json(line))
    return samples


def _make_runner_mock(response_text=""):
    runner = MagicMock()
    runner.generate.return_value = {
        "text": response_text,
        "tool_calls": [],
        "latency_ms": 100,
        "input_tokens": 10,
        "output_tokens": 20,
    }
    return runner


class TestSchemaValidation:
    def test_jsonl_schema_valid(self):
        samples = _load_samples()
        assert len(samples) >= 2
        for s in samples:
            assert s.task_type == "tool_call"
            assert s.difficulty in ("easy", "medium", "hard")
            assert s.user_query


class TestGraderIntegration:
    def setup_method(self):
        self.samples = _load_samples()
        self.runner = _make_runner_mock()
        self.evaluator = ToolCallEvaluator(
            runner=self.runner, model_name="test", checkpoint_name="base"
        )

    def test_build_prompt(self):
        for sample in self.samples:
            sys_prompt, user_prompt = self.evaluator.build_prompt(sample)
            assert sample.user_query in user_prompt

    def test_grade_returns_metrics(self):
        sample = self.samples[0]
        self.runner.generate.return_value = {
            "text": '{"tool_calls": [{"name": "query_expenses", "arguments": {"min_amount": 500000}}]}',
            "tool_calls": [],
            "latency_ms": 100,
            "input_tokens": 10,
            "output_tokens": 20,
        }
        result = self.evaluator.run_one(sample)

        assert "tool_selection_accuracy" in result.metric_values
        assert "argument_validity" in result.metric_values
        assert "schema_validity" in result.metric_values
        assert "task_success" in result.metric_values
        assert result.metric_values["tool_selection_accuracy"] == 1.0

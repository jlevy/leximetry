"""
End-to-end tests of evaluate_text without requiring a real API key.

TestModel exercises the orchestration path; FunctionModel captures the
prompt that would be sent to the LLM, locking down its content as a
contract before the prompts get refactored into their own module.
"""

from __future__ import annotations

from typing import Any, cast
from unittest.mock import patch

import pytest
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
from pydantic_ai.models.function import AgentInfo, FunctionModel
from pydantic_ai.models.test import TestModel

from leximetry.eval.evaluate_text import evaluate_text
from leximetry.eval.metrics_model import ProseMetrics, load_scoring_rubric

SAMPLE_TEXT = (
    "The history of writing systems is long and varied. "
    "Cuneiform, developed in ancient Mesopotamia, is among the earliest known scripts. "
    "Egyptian hieroglyphs followed soon after, originating roughly five thousand years ago. "
    "Different cultures independently developed methods for recording language, "
    "from logographic systems in China to alphabetic systems in the Mediterranean. "
    "Each system reflects the linguistic and cultural needs of the society that produced it. "
    "Modern writing systems continue to evolve as new technologies and communication "
    "needs emerge across the globe."
)


def test_evaluate_text_e2e_with_test_model():
    """
    Full pipeline against pydantic-ai TestModel, using a fixed score response.

    Asserts every one of the 12 metrics gets populated through the
    parse-and-assemble path; this is what would catch a regression in
    Agent.run() between pydantic-ai versions.
    """
    test_model = TestModel(custom_output_text="4 (Mocked rationale.)")

    with patch("leximetry.eval.evaluate_text.infer_model", return_value=test_model):
        result = evaluate_text(SAMPLE_TEXT, model="ignored-by-mock")

    assert isinstance(result, ProseMetrics)

    for group_name in ("expression", "style", "groundedness", "impact"):
        group = getattr(result, group_name)
        group_fields = cast(dict[str, Any], type(group).model_fields)
        for metric_name in group_fields:
            score = getattr(group, metric_name)
            assert score.value == 4, f"{group_name}.{metric_name} got value {score.value}"
            assert score.note == "Mocked rationale.", (
                f"{group_name}.{metric_name} got note {score.note!r}"
            )


def test_evaluate_text_rejects_short_input():
    """Short text should be rejected before any model call."""
    with pytest.raises(ValueError, match="too short"):
        evaluate_text("Two short sentences. Not enough.", model="ignored")


def test_prompt_contract():
    """
    Capture the prompts dispatched to the model and assert their content
    structure. This locks down the prompt-as-contract before prompts get
    extracted into their own module in the library refactor.
    """
    captured: list[str] = []

    def capture(messages: list[ModelMessage], _info: AgentInfo) -> ModelResponse:
        for msg in messages:
            if isinstance(msg, ModelRequest):
                for part in msg.parts:
                    if isinstance(part, UserPromptPart):
                        prompt = (
                            part.content if isinstance(part.content, str) else str(part.content)
                        )
                        captured.append(prompt)
        return ModelResponse(parts=[TextPart(content="3 (Captured.)")])

    function_model = FunctionModel(capture)

    with patch("leximetry.eval.evaluate_text.infer_model", return_value=function_model):
        evaluate_text(SAMPLE_TEXT, model="ignored-by-mock")

    rubric = load_scoring_rubric()
    assert len(captured) == len(rubric.metrics) == 12, (
        f"expected one prompt per metric; got {len(captured)}"
    )

    rubric_by_name = {m.name: m for m in rubric.metrics}
    metric_names_seen: set[str] = set()
    for prompt in captured:
        # Each prompt must include the source text we are evaluating.
        assert SAMPLE_TEXT in prompt, "prompt missing the text under evaluation"
        # The output-format instruction must be present so the LLM returns
        # something Score.parse can actually parse.
        assert "SCORE (REASON)" in prompt, "prompt missing output-format instruction"
        # And one and only one metric description must match.
        matches = [name for name, m in rubric_by_name.items() if m.description in prompt]
        assert len(matches) == 1, (
            f"prompt should reference exactly one metric description; got {matches}"
        )
        metric_name = matches[0]
        metric_names_seen.add(metric_name)
        # All six score levels (0-5) for that metric must appear in the prompt.
        for level, level_text in rubric_by_name[metric_name].values.items():
            assert f"{level}: {level_text}" in prompt, (
                f"prompt for {metric_name} missing score level {level}"
            )

    # Every metric was dispatched exactly once.
    assert metric_names_seen == set(rubric_by_name), (
        f"missing metric prompts: {set(rubric_by_name) - metric_names_seen}"
    )

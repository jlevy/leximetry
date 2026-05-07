"""
End-to-end test of evaluate_text using pydantic-ai's TestModel.

This catches behavioral changes across pydantic-ai versions (e.g. 0.3 -> 1.x)
without requiring a real API key. It exercises the full orchestration:
prompt construction per metric, parallel rate-limited dispatch, response
parsing, and assembly into a ProseMetrics object.
"""

from __future__ import annotations

from typing import Any, cast
from unittest.mock import patch

import pytest
from pydantic_ai.models.test import TestModel

from leximetry.eval.evaluate_text import evaluate_text
from leximetry.eval.metrics_model import ProseMetrics

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

"""
Tests that the rubric source-of-truth (JSON loaded by load_scoring_rubric)
aligns with the Pydantic model structure (ProseMetrics groups + fields).

This catches drift in either direction: a metric added to leximetry.md
without a corresponding Pydantic field, or a Pydantic field added without
a rubric entry. Either drift would silently produce a Score(value=0,
note="Not evaluated") for the affected metric in production.
"""

from __future__ import annotations

from typing import Any, cast

from leximetry.eval.metrics_model import (
    Expression,
    Groundedness,
    Impact,
    ProseMetrics,
    Style,
    load_scoring_rubric,
)

EXPECTED_METRIC_COUNT = 12
EXPECTED_GROUPS = ("expression", "style", "groundedness", "impact")


def _all_pydantic_metric_names() -> set[str]:
    names: set[str] = set()
    for group_cls in (Expression, Style, Groundedness, Impact):
        fields = cast(dict[str, Any], group_cls.model_fields)
        names.update(fields.keys())
    return names


def test_rubric_metric_count():
    rubric = load_scoring_rubric()
    assert len(rubric.metrics) == EXPECTED_METRIC_COUNT


def test_rubric_metrics_match_pydantic_fields():
    """
    Every rubric metric (case-insensitive) must have a matching Pydantic field;
    every Pydantic metric field must have a matching rubric entry.
    """
    rubric = load_scoring_rubric()
    rubric_names = {m.name.lower() for m in rubric.metrics}
    pydantic_names = _all_pydantic_metric_names()

    missing_in_pydantic = rubric_names - pydantic_names
    missing_in_rubric = pydantic_names - rubric_names

    assert not missing_in_pydantic, f"rubric metrics with no Pydantic field: {missing_in_pydantic}"
    assert not missing_in_rubric, f"Pydantic fields with no rubric metric: {missing_in_rubric}"


def test_rubric_score_levels_complete():
    """Every metric must define exactly score levels 0..5."""
    rubric = load_scoring_rubric()
    for metric in rubric.metrics:
        assert set(metric.values.keys()) == {0, 1, 2, 3, 4, 5}, (
            f"{metric.name} score levels: {sorted(metric.values.keys())}"
        )
        for level, text in metric.values.items():
            assert text.strip(), f"{metric.name} score {level} has empty text"


def test_prose_metrics_groups():
    """ProseMetrics must have exactly the four expected groups."""
    fields = cast(dict[str, Any], ProseMetrics.model_fields)
    assert tuple(fields.keys()) == EXPECTED_GROUPS

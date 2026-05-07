"""
Tests for the rich-rendered report output.

The existing test_compact_format in report_output.py only verifies that
rendering doesn't raise (and pulls in tiktoken via document stats, which
needs network). These tests render to an in-memory string and assert that
key labels actually appear in the output, providing real coverage of the
renderer post rich-15 / pydantic-2.13 upgrade.
"""

from __future__ import annotations

from rich.console import Console

from leximetry.cli.rich_styles import LEXIMETRY_THEME
from leximetry.eval.metrics_model import (
    Expression,
    Groundedness,
    Impact,
    ProseMetrics,
    Score,
    Style,
)
from leximetry.eval.report_output import (
    format_prose_metrics_plain,
    format_prose_metrics_rich,
)


def _sample_metrics() -> ProseMetrics:
    return ProseMetrics(
        expression=Expression(
            clarity=Score(value=5, note="Crisp prose."),
            coherence=Score(value=4, note="Mostly follows."),
            sincerity=Score(value=3, note=""),
        ),
        style=Style(
            subjectivity=Score(value=2, note="Largely objective."),
            narrativity=Score(value=1, note=""),
            warmth=Score(value=4, note="Warm tone."),
        ),
        groundedness=Groundedness(
            factuality=Score(value=4, note="Cited."),
            rigor=Score(value=3, note=""),
            depth=Score(value=5, note="Thorough."),
        ),
        impact=Impact(
            sensitivity=Score(value=1, note=""),
            accessibility=Score(value=4, note="Accessible."),
            longevity=Score(value=3, note=""),
        ),
    )


def _render_rich(metrics: ProseMetrics) -> str:
    console = Console(theme=LEXIMETRY_THEME, record=True, width=80)
    console.print(format_prose_metrics_rich(metrics))
    return console.export_text()


def test_rich_renderer_includes_title_and_groups():
    output = _render_rich(_sample_metrics())
    assert "Leximetry" in output
    for group in ("EXPRESSION", "STYLE", "GROUNDEDNESS", "IMPACT"):
        assert group in output, f"missing group label {group!r}"


def test_rich_renderer_includes_all_metric_names():
    output = _render_rich(_sample_metrics()).lower()
    metrics = (
        "clarity",
        "coherence",
        "sincerity",
        "subjectivity",
        "narrativity",
        "warmth",
        "factuality",
        "rigor",
        "depth",
        "sensitivity",
        "accessibility",
        "longevity",
    )
    for name in metrics:
        assert name in output, f"missing metric label {name!r}"


def test_rich_renderer_includes_notes():
    output = _render_rich(_sample_metrics())
    for snippet in ("Crisp prose.", "Mostly follows.", "Largely objective.", "Cited."):
        assert snippet in output, f"missing note snippet {snippet!r}"


def test_plain_renderer_round_trip():
    """The plain renderer is plumbed but lightly used; lock it down."""
    output = format_prose_metrics_plain(_sample_metrics())
    assert "Leximetry" in output
    assert "Clarity" in output
    assert "Crisp prose." in output
    # Score values appear in the form "(N)".
    assert "(5)" in output
    assert "(1)" in output

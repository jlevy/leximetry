from __future__ import annotations

import json
import re
from functools import cache
from pathlib import Path

from pydantic import BaseModel, Field


class Score(BaseModel):
    """
    A score with both numeric value and explanation.
    """

    value: int = Field(..., ge=0, le=5)
    note: str = Field(default="")

    @classmethod
    def parse(cls, text: str) -> Score:
        """
        Parse score from LLM output in format "SCORE (EXPLANATION)" or just "SCORE".

        Examples:
        - "5 (Well written. No language errors.)"
        - "3 (Contains speculations about the authors cat as well as factual content on C++ programming.)"
        - "1"
        - "4 (Clear reasoning but some gaps)"
        """
        text = text.strip()

        # Try to match "SCORE (EXPLANATION)" format
        match = re.match(r"^(\d+)\s*\(([^)]*)\)\s*$", text)
        if match:
            value = int(match.group(1))
            note = match.group(2).strip()
            return cls(value=value, note=note)

        # Try to match just a number
        match = re.match(r"^(\d+)\s*$", text)
        if match:
            value = int(match.group(1))
            return cls(value=value, note="")

        # Try to extract first number if format is unclear
        numbers = re.findall(r"\d+", text)
        if numbers:
            value = int(numbers[0])
            # Try to extract text after the number as explanation
            # Remove everything up to and including the first number and any following punctuation/spaces
            remaining = re.sub(r"^.*?\d+\s*[:\-\(\)\s]*", "", text).strip()
            return cls(value=value, note=remaining)

        # Fallback: return 0 with the original text as note
        return cls(value=0, note=text)


class Expression(BaseModel):
    clarity: Score = Field(default_factory=lambda: Score(value=0))
    coherence: Score = Field(default_factory=lambda: Score(value=0))
    sincerity: Score = Field(default_factory=lambda: Score(value=0))


class Style(BaseModel):
    subjectivity: Score = Field(default_factory=lambda: Score(value=0))
    narrativity: Score = Field(default_factory=lambda: Score(value=0))
    warmth: Score = Field(default_factory=lambda: Score(value=0))


class Groundedness(BaseModel):
    factuality: Score = Field(default_factory=lambda: Score(value=0))
    thoroughness: Score = Field(default_factory=lambda: Score(value=0))
    rigor: Score = Field(default_factory=lambda: Score(value=0))


class Impact(BaseModel):
    sensitivity: Score = Field(
        default_factory=lambda: Score(value=0)
    )  # Maps to "Sensitivity" in rubric
    accessibility: Score = Field(default_factory=lambda: Score(value=0))
    longevity: Score = Field(default_factory=lambda: Score(value=0))


class ProseMetrics(BaseModel):
    """
    Abstract metrics for prose. See `leximetry.md` for more details.
    """

    expression: Expression
    style: Style
    groundedness: Groundedness
    impact: Impact


class MetricRubric(BaseModel):
    """
    Rubric definition for a single metric.
    """

    name: str
    description: str
    values: dict[int, str]  # value number (0-5) -> description


class ScoringRubric(BaseModel):
    """
    Complete scoring rubric containing all metric definitions.
    """

    metrics: list[MetricRubric]


@cache
def load_scoring_rubric() -> ScoringRubric:
    """
    Load the scoring rubric from the JSON file.
    """
    current_file = Path(__file__)
    rubric_path = current_file.parent.parent / "docs" / "scoring_rubric.json"
    rubric_data = json.loads(rubric_path.read_text())
    return ScoringRubric.model_validate(rubric_data)


## Tests


def test_score_parsing():
    """Test Score.parse method with various inputs."""
    # Standard format
    score1 = Score.parse("5 (Well written. No language errors.)")
    assert score1.value == 5
    assert score1.note == "Well written. No language errors."

    # Just a number
    score2 = Score.parse("3")
    assert score2.value == 3
    assert score2.note == ""

    # Number with spaces
    score3 = Score.parse("  4  ")
    assert score3.value == 4
    assert score3.note == ""

    # Complex explanation
    score4 = Score.parse("2 (Contains some factual content but also speculative elements)")
    assert score4.value == 2
    assert score4.note == "Contains some factual content but also speculative elements"

    # Malformed but extractable
    score5 = Score.parse("Score: 4 - generally well structured")
    assert score5.value == 4
    assert score5.note == "generally well structured"

    # No number found
    score6 = Score.parse("unclear input")
    assert score6.value == 0
    assert score6.note == "unclear input"


def test_prose_metrics():
    """Test serialization and deserialization of ProseMetrics."""
    # Create test data
    original = ProseMetrics(
        expression=Expression(
            clarity=Score(value=4, note="Clear writing"),
            coherence=Score(value=3, note="Generally follows"),
            sincerity=Score(value=5, note="Authentic tone"),
        ),
        style=Style(
            subjectivity=Score(value=3, note="Mix of objective and personal"),
            narrativity=Score(value=2, note="Mostly factual"),
            warmth=Score(value=4, note="Positive tone"),
        ),
        groundedness=Groundedness(
            factuality=Score(value=3, note="Some verifiable facts"),
            thoroughness=Score(value=2, note="Brief treatment"),
            rigor=Score(value=4, note="Well-structured reasoning"),
        ),
        impact=Impact(
            sensitivity=Score(value=4, note="Some sensitive content"),
            accessibility=Score(value=3, note="Some background needed"),
            longevity=Score(value=2, note="Relevant for weeks"),
        ),
    )

    # Test serialization
    json_str = original.model_dump_json()

    # Test deserialization
    reconstructed = ProseMetrics.model_validate_json(json_str)

    # Verify they match
    assert original == reconstructed
    assert reconstructed.expression.clarity.value == 4
    assert reconstructed.expression.clarity.note == "Clear writing"
    assert reconstructed.groundedness.factuality.value == 3
    assert reconstructed.style.narrativity.note == "Mostly factual"

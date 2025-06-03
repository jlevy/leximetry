import json
from functools import cache
from pathlib import Path

from pydantic import BaseModel, Field


class Expression(BaseModel):
    clarity: int = Field(..., ge=0, le=5)
    coherence: int = Field(..., ge=0, le=5)
    sincerity: int = Field(..., ge=0, le=5)


class Style(BaseModel):
    narrativity: int = Field(..., ge=0, le=5)
    subjectivity: int = Field(..., ge=0, le=5)
    warmth: int = Field(..., ge=0, le=5)


class Groundedness(BaseModel):
    factuality: int = Field(..., ge=0, le=5)
    rigor: int = Field(..., ge=0, le=5)
    thoroughness: int = Field(..., ge=0, le=5)


class Impact(BaseModel):
    accessibility: int = Field(..., ge=0, le=5)
    longevity: int = Field(..., ge=0, le=5)
    harmlessness: int = Field(..., ge=0, le=5)


class ProseMetrics(BaseModel):
    """
    Abstract metrics for prose. See `prose_metrics.md` for more details.
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
    values: dict[int, str]  # value number (1-5) -> description


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


def test_prose_metrics():
    """Test serialization and deserialization of ProseMetrics."""
    # Create test data
    original = ProseMetrics(
        expression=Expression(clarity=4, coherence=3, sincerity=5),
        style=Style(narrativity=2, subjectivity=3, warmth=4),
        groundedness=Groundedness(factuality=3, rigor=4, thoroughness=2),
        impact=Impact(accessibility=3, longevity=2, harmlessness=4),
    )

    # Test serialization
    json_str = original.model_dump_json()
    expected_structure = {
        "expression": {"clarity": 4, "coherence": 3, "sincerity": 5},
        "style": {"narrativity": 2, "subjectivity": 3, "warmth": 4},
        "groundedness": {"factuality": 3, "rigor": 4, "thoroughness": 2},
        "impact": {"accessibility": 3, "longevity": 2, "harmlessness": 4},
    }

    # Test deserialization
    reconstructed = ProseMetrics.model_validate_json(json_str)

    # Verify they match
    assert original == reconstructed
    assert original.model_dump() == expected_structure
    assert reconstructed.expression.clarity == 4
    assert reconstructed.groundedness.factuality == 3
    assert reconstructed.style.narrativity == 2
    assert reconstructed.impact.accessibility == 3

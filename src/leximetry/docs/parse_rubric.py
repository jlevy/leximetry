import json
import re
from pathlib import Path
from typing import Any

from leximetry.model.metrics_model import MetricRubric, ScoringRubric


def parse_scoring_rubric(markdown_content: str) -> ScoringRubric:
    """
    Quick hack to parse the scoring rubric section from the prose metrics markdown.
    """

    # Find the scoring rubric section - it goes until the next major section or end
    rubric_match = re.search(
        r"### Scoring Rubric\n\n(.*?)(?=\n###|\n##|$)", markdown_content, re.DOTALL
    )
    if not rubric_match:
        raise ValueError("Could not find '### Scoring Rubric' section")

    rubric_content = rubric_match.group(1)

    # Parse individual metrics
    metrics: list[MetricRubric] = []

    # Find all metric sections using a more robust pattern
    # Updated pattern to make the trailing newlines optional for the last value
    metric_pattern = r"- \*\*Metric:\*\* (.+?)\n\n  - \*\*Description:\*\* (.+?)\n\n((?:  - \*\*Value \d+:\*\* .+?(?:\n\n|$))+)"

    for match in re.finditer(metric_pattern, rubric_content, re.DOTALL):
        name = match.group(1).strip()
        description = match.group(2).strip()
        values_section = match.group(3)

        # Parse the values
        values: dict[int, str] = {}
        # Use a more flexible pattern that doesn't require trailing newlines
        value_pattern = (
            r"  - \*\*Value (\d+):\*\* (.+?)(?=\n  - \*\*Value \d+:\*\*|\n- \*\*Metric:\*\*|$)"
        )

        for value_match in re.finditer(value_pattern, values_section, re.DOTALL):
            value_num = int(value_match.group(1))
            value_text = value_match.group(2).strip()
            # Remove extra whitespace and join multi-line descriptions
            value_text = " ".join(value_text.split())
            values[value_num] = value_text

        if values:  # Only add if we found values
            metric = MetricRubric(name=name, description=description, values=values)
            metrics.append(metric)

    return ScoringRubric(metrics=metrics)


def extract_rubric_to_json(
    prose_metrics_path: str | Path, output_path: str | Path | None = None
) -> dict[str, Any]:
    """
    Extract scoring rubric from prose_metrics.md and save as JSON.

    Returns the parsed rubric as a dictionary.
    """

    prose_metrics_path = Path(prose_metrics_path)
    markdown_content = prose_metrics_path.read_text(encoding="utf-8")

    rubric = parse_scoring_rubric(markdown_content)
    rubric_dict = rubric.model_dump()

    if output_path:
        output_path = Path(output_path)
        json_str = json.dumps(rubric_dict, indent=2)
        output_path.write_text(json_str, encoding="utf-8")
        print(f"Scoring rubric saved to {output_path}")

    return rubric_dict


def main():
    """
    Main function to generate the scoring rubric JSON from prose_metrics.md.
    """
    # Find the prose_metrics.md file
    current_file = Path(__file__)
    docs_dir = current_file.parent.parent / "docs"
    prose_metrics_path = docs_dir / "prose_metrics.md"
    output_path = docs_dir / "scoring_rubric.json"

    # Extract and save the rubric
    rubric_dict = extract_rubric_to_json(prose_metrics_path, output_path)

    # Print summary
    print(f"Extracted scoring rubric with {len(rubric_dict['metrics'])} metrics:")
    for i, metric in enumerate(rubric_dict["metrics"], 1):
        print(f"  {i:2d}. {metric['name']}: {len(metric['values'])} value levels")

    print(f"Saved to: {output_path}")

    # Verify JSON structure
    rubric = ScoringRubric.model_validate(rubric_dict)
    assert len(rubric.metrics) == len(rubric_dict["metrics"])

    print("All validations passed!")


## Tests


def test_scoring_rubric_models():
    """Test the scoring rubric Pydantic models."""
    # Create test data
    test_metric = MetricRubric(
        name="Clarity",
        description="Is the language readable and clear?",
        values={
            0: "Cannot assess",
            1: "Contains numerous errors",
            2: "Contains errors but is clear",
            3: "Typical business email quality",
            4: "Clear, correct language",
            5: "Perfect grammar and clarity",
        },
    )

    rubric = ScoringRubric(metrics=[test_metric])

    # Test serialization
    json_str = rubric.model_dump_json()

    # Test deserialization
    reconstructed = ScoringRubric.model_validate_json(json_str)

    # Verify they match
    assert rubric == reconstructed
    assert reconstructed.metrics[0].name == "Clarity"
    assert reconstructed.metrics[0].values[0] == "Cannot assess"
    assert reconstructed.metrics[0].values[1] == "Contains numerous errors"


def test_extract_full_rubric():
    """Test extraction from the actual prose_metrics.md file."""

    # Find the prose_metrics.md file
    current_file = Path(__file__)
    docs_dir = current_file.parent.parent / "docs"
    prose_metrics_path = docs_dir / "prose_metrics.md"

    if not prose_metrics_path.exists():
        print(f"Skipping test - file not found: {prose_metrics_path}")
        return

    # Extract rubric without saving to file
    rubric_dict = extract_rubric_to_json(prose_metrics_path)

    # Basic structure verification
    assert "metrics" in rubric_dict
    metrics = rubric_dict["metrics"]
    assert len(metrics) == 12, f"Expected exactly 12 metrics, got {len(metrics)}"

    # Verify each metric has proper structure and data
    for metric in metrics:
        assert "name" in metric and metric["name"]
        assert "description" in metric and metric["description"]
        assert "values" in metric
        assert isinstance(metric["values"], dict)

        # Check that each metric has exactly 6 values (0-5)
        values = metric["values"]
        assert len(values) == 6, (
            f"Metric {metric['name']} should have 6 values (0-5), but has {len(values)}"
        )

        # Values should be 0, 1, 2, 3, 4, 5
        for i in range(6):
            assert i in values
            assert values[i].strip()

    # Test round-trip through Pydantic model
    rubric = ScoringRubric.model_validate(rubric_dict)
    assert len(rubric.metrics) == len(metrics)

    print(f"✓ Successfully extracted {len(metrics)} metrics from actual docs")
    print("✓ All metrics have exactly 6 value levels (0-5)")


def test_save_rubric_to_json():
    """Test saving rubric to JSON file."""

    import tempfile

    # Find the prose_metrics.md file
    current_file = Path(__file__)
    docs_dir = current_file.parent.parent / "docs"
    prose_metrics_path = docs_dir / "prose_metrics.md"

    if not prose_metrics_path.exists():
        print(f"Skipping test - file not found: {prose_metrics_path}")
        return

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as tmp_file:
        tmp_path = Path(tmp_file.name)

    try:
        # Extract and save rubric
        rubric_dict = extract_rubric_to_json(prose_metrics_path, tmp_path)

        # Verify the output file was created
        assert tmp_path.exists()

        # Verify the JSON is valid
        with tmp_path.open() as f:
            loaded_dict = json.load(f)

        # The JSON will have string keys, so we need to compare the structure rather than exact equality
        assert "metrics" in loaded_dict
        assert len(loaded_dict["metrics"]) == len(rubric_dict["metrics"])

        # Verify first metric as a spot check
        first_metric = loaded_dict["metrics"][0]
        assert "name" in first_metric
        assert "description" in first_metric
        assert "values" in first_metric

        # Verify the first metric has 6 values with string keys "0" through "5"
        values = first_metric["values"]
        assert len(values) == 6
        for i in range(6):
            assert str(i) in values

        print(f"✓ Successfully saved rubric to {tmp_path}")

    finally:
        # Clean up
        if tmp_path.exists():
            tmp_path.unlink()


if __name__ == "__main__":
    main()

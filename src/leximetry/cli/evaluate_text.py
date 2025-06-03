import asyncio
import json
from textwrap import dedent

from pydantic_ai import Agent
from pydantic_ai.models import Model, infer_model
from rich import print as rprint
from strif import abbrev_str

from leximetry.model.metrics_model import (
    Expression,
    Groundedness,
    Impact,
    MetricRubric,
    ProseMetrics,
    Style,
    load_scoring_rubric,
)


async def evaluate_single_metric(text: str, metric: MetricRubric, model: Model) -> tuple[str, int]:
    """
    Evaluate text for a single metric and return `(metric_name, score)`.
    """
    # Format the metric values for the prompt
    values_desc = "\n".join([f"{score}: {desc}" for score, desc in metric.values.items()])

    prompt = dedent(f"""
        Evaluate this text for the metric "{metric.name}".
        
        METRIC DESCRIPTION: {metric.description}
        
        SCORING SCALE:
        {values_desc}
        
        TEXT TO EVALUATE:
        {text}
        
        Return only the numeric score (1-{max(metric.values.keys())}) that best describes the text, using the scoring scale above.
        If there isn't enough text to assess this metric, return 0.
    """)

    # Create a simple agent for single metric evaluation
    single_metric_agent = Agent(
        model=model,
        output_type=int,
        instructions="You are evaluating metrics about a text excerpt. "
        "Return only the numeric score that best matches the criteria.",
    )

    rprint(f"Evaluating {metric.name} with prompt: {abbrev_str(prompt)}")
    result = await single_metric_agent.run(prompt)
    return metric.name.lower(), result.output


async def evaluate_text_async(text: str, model_name: str = "gpt-4o-mini") -> str:
    """
    Evaluate text by calling the LLM once for each metric and assembling results.
    The `model_name` is a Pydantic model name like "gpt-4o-mini" or "claude-3-5-sonnet-latest".
    """
    if not text.strip():
        return json.dumps({"error": "No text provided for evaluation"}, indent=2)

    rprint(f"Evaluating text with model: {model_name}")
    rprint(f"Text length: {len(text)} characters")

    try:
        # Load the scoring rubric
        scoring_rubric = load_scoring_rubric()

        # Create the model
        model = infer_model(model_name)

        rprint(f"Starting evaluation for {len(scoring_rubric.metrics)} metrics...")

        # Evaluate each metric individually (can be parallelized)
        metric_tasks = [
            evaluate_single_metric(text, metric, model) for metric in scoring_rubric.metrics
        ]

        # Run all metric evaluations in parallel
        metric_results = await asyncio.gather(*metric_tasks)

        # Assemble results into ProseMetrics object
        scores = dict(metric_results)

        # Create ProseMetrics instance with the scores mapped to the correct structure
        prose_metrics = ProseMetrics(
            expression=Expression(
                clarity=scores.get("clarity", 0),
                coherence=scores.get("coherence", 0),
                sincerity=scores.get("sincerity", 0),
            ),
            style=Style(
                narrativity=scores.get("narrativity", 0),
                subjectivity=scores.get("subjectivity", 0),
                warmth=scores.get("warmth", 0),
            ),
            groundedness=Groundedness(
                factuality=scores.get("factuality", 0),
                rigor=scores.get("rigor", 0),
                thoroughness=scores.get("thoroughness", 0),
            ),
            impact=Impact(
                accessibility=scores.get("accessibility", 0),
                longevity=scores.get("longevity", 0),
                harmlessness=scores.get("harmlessness", 0),
            ),
        )

        rprint("Evaluation completed successfully")
        return prose_metrics.model_dump_json(indent=2)

    except Exception as e:
        error_msg = f"Error during evaluation: {str(e)}"
        rprint(f"[red]{error_msg}[/red]")
        return json.dumps({"error": error_msg}, indent=2)


def evaluate_text(text: str, model: str = "gpt-4o-mini") -> str:
    """
    Synchronous wrapper for evaluate_text.
    """
    return asyncio.run(evaluate_text_async(text, model))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python evaluate_text.py <text> [model]")
        sys.exit(1)

    text_input = sys.argv[1]
    model_name = sys.argv[2] if len(sys.argv) > 2 else "gpt-4o-mini"

    result = evaluate_text(text_input, model_name)
    print(result)

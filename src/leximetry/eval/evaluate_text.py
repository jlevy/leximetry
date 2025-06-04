import asyncio
import time
from textwrap import dedent

from chopdiff.docs import TextDoc, TextUnit
from funlog import format_duration
from pydantic_ai import Agent
from pydantic_ai.models import Model, infer_model
from rich import print as rprint

from leximetry.eval.metrics_model import (
    Expression,
    Groundedness,
    Impact,
    MetricRubric,
    ProseMetrics,
    Score,
    Style,
    load_scoring_rubric,
)


async def evaluate_single_metric(
    text: str, metric: MetricRubric, model: Model
) -> tuple[str, Score]:
    """
    Evaluate text for a single metric and return `(metric_name, Score)`.
    """
    start_time = time.time()
    # Format the metric values for the prompt
    values_desc = "\n".join([f"{score}: {desc}" for score, desc in metric.values.items()])

    prompt = dedent(f"""
        Evaluate this text for the metric "{metric.name}".
        
        METRIC DESCRIPTION: {metric.description}
        
        SCORING SCALE:
        {values_desc}
        
        TEXT TO EVALUATE:
        {text}
        
        Provide a result in the form "SCORE (REASON)":
        - The score as a single digit (0-5) that best describes the text using the scoring scale above
        - A brief parenthetical note with one or two sentences mentioning the reason for the score
        
        If there isn't enough text to assess this metric, return "0 (Insufficient content)".
        
        Examples:
        - "5 (Well written. No language errors.)"
        - "3 (Contains speculations about the author's cat as well as factual content.)"
        - "1 (Technical paper with clear structure.)"
    """)

    # Create a simple agent for single metric evaluation
    single_metric_agent = Agent(
        model=model,
        output_type=str,
        instructions="You are evaluating metrics about a text excerpt. "
        "Return your response in the exact format: SCORE (REASON) where SCORE is 0-5 and REASON is a brief explanation.",
    )

    result = await single_metric_agent.run(prompt)

    # Parse the LLM response into a Score object
    score = Score.parse(result.output)

    # Map metric name to lowercase for consistent lookup
    metric_key = metric.name.lower()

    elapsed = time.time() - start_time
    print(f"Evaluated {metric_key} in {format_duration(elapsed)}")
    return metric_key, score


async def evaluate_text_async(text: str, model_name: str = "gpt-4o-mini") -> ProseMetrics:
    """
    Evaluate text by calling the LLM once for each metric and assembling results.
    The `model_name` is a Pydantic model name like "gpt-4o-mini" or "claude-3-5-sonnet-latest".
    """
    if not text.strip():
        raise ValueError("No text provided for evaluation")

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
                clarity=scores.get("clarity", Score(value=0, note="Not evaluated")),
                coherence=scores.get("coherence", Score(value=0, note="Not evaluated")),
                sincerity=scores.get("sincerity", Score(value=0, note="Not evaluated")),
            ),
            style=Style(
                narrativity=scores.get("narrativity", Score(value=0, note="Not evaluated")),
                subjectivity=scores.get("subjectivity", Score(value=0, note="Not evaluated")),
                warmth=scores.get("warmth", Score(value=0, note="Not evaluated")),
            ),
            groundedness=Groundedness(
                factuality=scores.get("factuality", Score(value=0, note="Not evaluated")),
                rigor=scores.get("rigor", Score(value=0, note="Not evaluated")),
                thoroughness=scores.get("thoroughness", Score(value=0, note="Not evaluated")),
            ),
            impact=Impact(
                accessibility=scores.get("accessibility", Score(value=0, note="Not evaluated")),
                longevity=scores.get("longevity", Score(value=0, note="Not evaluated")),
                sensitivity=scores.get("sensitivity", Score(value=0, note="Not evaluated")),
            ),
        )

        rprint("Evaluation complete!")
        rprint()

        return prose_metrics

    except Exception as e:
        error_msg = f"Error during evaluation: {str(e)}"
        rprint(f"[red]{error_msg}[/red]")
        raise


def evaluate_text(text: str, model: str = "gpt-4o-mini") -> ProseMetrics:
    """
    Synchronous wrapper for evaluate_text_async.
    """

    doc = TextDoc.from_text(text)
    if doc.size(TextUnit.words) < 50:
        raise ValueError("Text is < 50 words so too short to evaluate")
    if doc.size(TextUnit.sentences) < 3:
        raise ValueError("Text is < 3 sentences so too short to evaluate")

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

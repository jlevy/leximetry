from __future__ import annotations

from textwrap import wrap
from typing import TYPE_CHECKING

from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from leximetry.cli.rich_styles import COLOR_SCHEME, GROUP_HEADERS

if TYPE_CHECKING:
    from leximetry.eval.metrics_model import ProseMetrics, Score

METRICS_TITLE = "Leximetry"

# Define the group order and their metrics
GROUPS_CONFIG = {
    "expression": ["clarity", "coherence", "sincerity"],
    "style": ["subjectivity", "narrativity", "warmth"],
    "groundedness": ["factuality", "thoroughness", "rigor"],
    "impact": ["sensitivity", "accessibility", "longevity"],
}


def format_score_viz(value: int, char: str = "◆", reversed: bool = False) -> str:
    """
    Format score as a bar showing filled and empty positions out of 5.
    Returns filled diamonds followed by empty diamonds, or reversed if requested.
    """
    filled = char * value
    empty = "◇" * (5 - value)

    if reversed:
        return empty + filled
    else:
        return filled + empty


def format_score_rich(metric_name: str, value: int) -> Text:
    """
    Format a single score with rich formatting.
    """
    color = COLOR_SCHEME.get(metric_name.lower(), "white")
    diamonds = format_score_viz(value)

    text = Text()
    # Calculate padding to align diamonds vertically
    # Longest is "Subjectivity: 5 " = 16 chars
    metric_with_number = f"{metric_name.title()}: {value} "
    text.append(f"{metric_with_number:<16}", style="bold")
    text.append(diamonds, style=f"bold {color}")

    return text


def format_group_rich(group_name: str, scores: dict[str, tuple[int, str]]) -> Text:
    """
    Format a group of scores without panel wrapping.
    """
    title, title_color = GROUP_HEADERS[group_name.lower()]

    # Create group header
    content = Text()
    content.append(f"{title.upper()}", style=f"bold {title_color}")
    content.append("\n")

    # Add scores (without notes)
    for i, (metric_name, (value, _note)) in enumerate(scores.items()):
        if i > 0:
            content.append("\n")
        formatted_score = format_score_rich(metric_name, value)
        content.append(formatted_score)

    return content


def collect_notes(prose_metrics: ProseMetrics) -> list[tuple[str, str]]:
    """
    Collect all notes from the prose metrics.
    """
    notes: list[tuple[str, str]] = []

    for group_name, metric_names in GROUPS_CONFIG.items():
        group = getattr(prose_metrics, group_name)
        for metric_name in metric_names:
            score = getattr(group, metric_name)
            if score.note:
                notes.append((metric_name.title(), score.note))

    return notes


def format_notes_section(notes: list[tuple[str, str]]) -> RenderableType | None:
    """
    Format the notes section in horizontally paired columns with balanced heights.
    """
    if not notes:
        return None

    # Create a dict for easy lookup
    notes_dict = {metric_name: note for metric_name, note in notes}

    # Define the horizontal pairs based on metric positions
    pairs = [
        ("Clarity", "Factuality"),
        ("Coherence", "Thoroughness"),
        ("Sincerity", "Rigor"),
        ("Subjectivity", "Sensitivity"),
        ("Narrativity", "Accessibility"),
        ("Warmth", "Longevity"),
    ]

    # Available width for each column
    column_width = 30

    def format_single_note(metric_name: str, note: str) -> tuple[Text, int]:
        """Format a single note and return content plus line count"""
        content = Text()

        # Get the style name for this metric from the theme
        metric_style = COLOR_SCHEME.get(metric_name.lower(), "white")

        # Add metric name using the theme style
        content.append(f"{metric_name}:", style=metric_style)
        content.append("\n")

        # Wrap the note text
        wrapped_lines = wrap(note, width=column_width)

        for j, line in enumerate(wrapped_lines):
            if j > 0:
                content.append("\n")
            content.append(line, style="dim white")

        # Calculate total lines: 1 for name + 1 for newline + wrapped lines
        total_lines = 2 + len(wrapped_lines)

        return content, total_lines

    # Build all content
    all_content: list[tuple[Text, Text]] = []

    for left_metric, right_metric in pairs:
        left_note = notes_dict.get(left_metric, "")
        right_note = notes_dict.get(right_metric, "")

        # Only include pairs where at least one has a note
        if left_note or right_note:
            if left_note:
                left_content, left_height = format_single_note(left_metric, left_note)
            else:
                left_content, left_height = Text(), 0

            if right_note:
                right_content, right_height = format_single_note(right_metric, right_note)
            else:
                right_content, right_height = Text(), 0

            # Balance the pair by padding the shorter one
            height_diff = abs(left_height - right_height)
            if left_height < right_height:
                for _ in range(height_diff):
                    left_content.append("\n")
            elif right_height < left_height:
                for _ in range(height_diff):
                    right_content.append("\n")

            all_content.append((left_content, right_content))

    if not all_content:
        return None

    # Combine all pairs with spacing between them
    final_left = Text()
    final_right = Text()

    for i, (left_content, right_content) in enumerate(all_content):
        if i > 0:
            final_left.append("\n\n")
            final_right.append("\n\n")
        final_left.append(left_content)
        final_right.append(right_content)

    # Create header and columns
    header = Text()
    header.append("NOTES", style="bold dim white")
    header.append("\n")

    columns_display = Columns([final_left, final_right], equal=True, expand=False)

    return Group(header, columns_display)


def format_prose_metrics_rich(prose_metrics: ProseMetrics) -> RenderableType:
    """
    Format ProseMetrics object with rich formatting in mirrored two-column layout.
    """

    # Helper function to create a mirrored row layout
    def create_mirrored_section(
        left_group: str, right_group: str, include_headers: bool = True
    ) -> Text:
        left_title, _left_color = GROUP_HEADERS[left_group.lower()]
        right_title, _right_color = GROUP_HEADERS[right_group.lower()]
        left_metrics = GROUPS_CONFIG[left_group]
        right_metrics = GROUPS_CONFIG[right_group]
        left_data = getattr(prose_metrics, left_group)
        right_data = getattr(prose_metrics, right_group)

        content = Text()

        # Section headers aligned with labels (only if requested)
        if include_headers:
            content.append(f"{left_title.upper():>12}", style="bold dim white")
            content.append("                   ", style="dim white")
            content.append(f"{right_title.upper()}", style="bold dim white")
            content.append("\n")

        # Data rows
        for i in range(3):  # Each group has 3 metrics
            left_metric = left_metrics[i]
            right_metric = right_metrics[i]
            left_score = getattr(left_data, left_metric)
            right_score = getattr(right_data, right_metric)

            left_style = COLOR_SCHEME.get(left_metric.lower(), "white")
            right_style = COLOR_SCHEME.get(right_metric.lower(), "white")

            # Create styled diamond displays
            left_empty_count = 5 - left_score.value
            left_filled_count = left_score.value
            right_filled_count = right_score.value
            right_empty_count = 5 - right_score.value

            # Left side: right-aligned name in 12 chars, then diamonds and number
            left_name = left_metric.title()

            content.append(f"{left_name:>12}", style=left_style)
            content.append(" ", style="white")
            # Left side: empty diamonds first, then filled (reversed)
            if left_empty_count > 0:
                content.append("◇" * left_empty_count, style="dim white")
            if left_filled_count > 0:
                content.append("◆" * left_filled_count, style=left_style)
            content.append(f" {left_score.value}", style=left_style)
            content.append(" │ ", style="dim white")

            # Right side: number, diamonds, left-aligned name
            right_name = right_metric.title()

            content.append(f"{right_score.value} ", style=right_style)
            # Right side: filled diamonds first, then empty (normal)
            if right_filled_count > 0:
                content.append("◆" * right_filled_count, style=right_style)
            if right_empty_count > 0:
                content.append("◇" * right_empty_count, style="dim white")
            content.append(f" {right_name}", style=right_style)

            # Only add newline if not the last row
            if i < 2:
                content.append("\n")

        return content

    # Create the two mirrored sections
    top_section = create_mirrored_section("expression", "groundedness", include_headers=True)

    # Add horizontal separator
    separator = Text()
    separator.append("       STYLE", style="bold dim white")
    separator.append(" ────────", style="dim white")
    separator.append("┼", style="dim white")
    separator.append("──────── ", style="dim white")
    separator.append("IMPACT        ", style="bold dim white")

    bottom_section = create_mirrored_section("style", "impact", include_headers=False)

    # Combine sections with the separator
    panel_content = Group(top_section, separator, bottom_section)

    main_panel = Panel(
        panel_content,
        title=f"[bold white]{METRICS_TITLE}[/bold white]",
        border_style="white",
        padding=(0, 1),
        width=50,
    )

    # Collect and format notes
    notes = collect_notes(prose_metrics)
    notes_section = format_notes_section(notes)

    # Combine main panel with notes section
    if notes_section:
        return Group(main_panel, "", notes_section)
    else:
        return main_panel


def format_prose_metrics_plain(prose_metrics: ProseMetrics) -> str:
    """
    Format ProseMetrics object as plain text.
    """
    lines: list[str] = []
    lines.append(METRICS_TITLE)
    lines.append("=" * 50)
    lines.append("")

    for group_name, metric_names in GROUPS_CONFIG.items():
        # Group header
        title, _ = GROUP_HEADERS[group_name]
        lines.append(title.upper())
        lines.append("-" * 20)

        group = getattr(prose_metrics, group_name)

        for metric_name in metric_names:
            score = getattr(group, metric_name)
            # Format metric name with appropriate padding
            formatted_name = f"{metric_name.title()}"
            # Adjust padding based on longest name in the group
            padding = 13 if metric_name == "subjectivity" else 12
            padded_name = f"{formatted_name:<{padding}}"

            lines.append(
                f"{padded_name}{format_score_viz(score.value)} ({score.value}) {score.note}"
            )

        lines.append("")

    return "\n".join(lines)


def format_score_standalone(score: Score) -> str:
    """
    Format a Score object for rich display.
    """
    diamonds = format_score_viz(score.value)
    if score.note:
        return f"{diamonds} ({score.value}) {score.note}"
    return f"{diamonds} ({score.value})"


def format_doc_stats(
    bytes_count: int, lines: int, paras: int, sents: int, words: int, tokens: int
) -> RenderableType:
    """
    Format document statistics in two columns.
    """
    from rich.columns import Columns

    # Left column: Bytes, Lines, Tokens
    left_content = Text()
    left_content.append("Bytes: ", style="dim white")
    left_content.append(f"{bytes_count:,}", style="bold white")
    left_content.append("\n")
    left_content.append("Lines: ", style="dim white")
    left_content.append(f"{lines:,}", style="bold white")
    left_content.append("\n")
    left_content.append("Tokens: ", style="dim white")
    left_content.append(f"{tokens:,}", style="bold white")

    # Right column: Paras, Sentences, Words
    right_content = Text()
    right_content.append("Paras: ", style="dim white")
    right_content.append(f"{paras:,}", style="bold white")
    right_content.append("\n")
    right_content.append("Sentences: ", style="dim white")
    right_content.append(f"{sents:,}", style="bold white")
    right_content.append("\n")
    right_content.append("Words: ", style="dim white")
    right_content.append(f"{words:,}", style="bold white")

    # Create two-column layout
    columns_display = Columns([left_content, right_content], equal=True, expand=False)

    doc_panel = Panel(
        columns_display,
        title="[bold white]Document Summary[/bold white]",
        border_style="white",
        padding=(0, 1),
        width=55,
    )

    return doc_panel


def format_complete_analysis(
    prose_metrics: ProseMetrics,
    bytes_count: int = 0,
    lines: int = 0,
    paras: int = 0,
    sents: int = 0,
    words: int = 0,
    tokens: int = 0,
) -> RenderableType:
    """
    Format complete analysis with document stats and prose metrics.
    """
    # Create document summary panel
    doc_panel = format_doc_stats(bytes_count, lines, paras, sents, words, tokens)

    # Create metrics panel
    metrics_panel = format_prose_metrics_rich(prose_metrics)

    # Combine with spacing
    return Group(doc_panel, "", metrics_panel)


## Tests


def test_compact_format():
    """Test the complete analysis format with document stats and metrics."""
    from rich.console import Console

    from leximetry.eval.metrics_model import (
        Expression,
        Groundedness,
        Impact,
        ProseMetrics,
        Score,
        Style,
    )

    # Create test data with some notes
    test_metrics = ProseMetrics(
        expression=Expression(
            clarity=Score(
                value=5,
                note="The text is well-written with perfect grammar, appropriate punctuation, and no spelling errors. It is clear and reads well, with a good command of the language.",
            ),
            coherence=Score(value=3, note=""),
            sincerity=Score(value=4, note=""),
        ),
        style=Style(
            narrativity=Score(value=3, note=""),
            subjectivity=Score(
                value=5,
                note="Contains extensive personal opinions and subjective viewpoints rather than objective facts.",
            ),
            warmth=Score(value=3, note=""),
        ),
        groundedness=Groundedness(
            factuality=Score(value=2, note=""),
            rigor=Score(value=3, note=""),
            thoroughness=Score(value=3, note=""),
        ),
        impact=Impact(
            accessibility=Score(value=3, note=""),
            longevity=Score(value=4, note=""),
            sensitivity=Score(value=1, note=""),
        ),
    )

    console = Console()
    # Test with sample document statistics
    console.print(
        format_complete_analysis(
            test_metrics,
            bytes_count=272532,
            lines=4383,
            paras=597,
            sents=981,
            words=23721,
            tokens=79288,
        )
    )

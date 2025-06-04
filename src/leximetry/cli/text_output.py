from __future__ import annotations

from textwrap import wrap
from typing import TYPE_CHECKING

from chopdiff.docs import TextDoc
from rich.align import Align
from rich.box import Box
from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from leximetry.cli.rich_styles import COLOR_SCHEME, GROUP_HEADERS

if TYPE_CHECKING:
    from leximetry.eval.metrics_model import ProseMetrics, Score

METRICS_TITLE = "Leximetry"
BOX_WIDTH = 64

# Diamond symbols for score visualization
FILLED_DIAMOND = "◆"
EMPTY_DIAMOND = "◇"

# Define the group order and their metrics
GROUPS_CONFIG = {
    "expression": ["clarity", "coherence", "sincerity"],
    "style": ["subjectivity", "narrativity", "warmth"],
    "groundedness": ["factuality", "thoroughness", "rigor"],
    "impact": ["sensitivity", "accessibility", "longevity"],
}


def render_diamonds(
    filled_count: int,
    empty_count: int,
    text: Text,
    filled_style: str,
    empty_style: str = "dim white",
    reversed: bool = False,
) -> None:
    """
    Helper function to render diamond symbols with appropriate styling.
    If reversed=True, renders empty diamonds first, then filled diamonds.
    If reversed=False, renders filled diamonds first, then empty diamonds.
    """
    if reversed:
        if empty_count > 0:
            text.append(EMPTY_DIAMOND * empty_count, style=empty_style)
        if filled_count > 0:
            text.append(FILLED_DIAMOND * filled_count, style=filled_style)
    else:
        if filled_count > 0:
            text.append(FILLED_DIAMOND * filled_count, style=filled_style)
        if empty_count > 0:
            text.append(EMPTY_DIAMOND * empty_count, style=empty_style)


def format_score_viz(value: int, char: str = FILLED_DIAMOND, reversed: bool = False) -> str:
    """
    Format score as a bar showing filled and empty positions out of 5.
    Returns filled diamonds followed by empty diamonds, or reversed if requested.
    """
    filled = char * value
    empty = EMPTY_DIAMOND * (5 - value)

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
    Format the notes section in horizontally paired columns with balanced heights and group headings.
    """
    if not notes:
        return None

    # Create a dict for easy lookup
    notes_dict = {metric_name: note for metric_name, note in notes}

    # Define the horizontal pairs based on metric positions, with group headings
    grid_rows = [
        # Group headers for first section
        ("__EXPRESSION_HEADER", "__GROUNDEDNESS_HEADER"),
        # Expression vs Groundedness metrics
        ("Clarity", "Factuality"),
        ("Coherence", "Thoroughness"),
        ("Sincerity", "Rigor"),
        # Group headers for second section
        ("__STYLE_HEADER", "__IMPACT_HEADER"),
        # Style vs Impact metrics
        ("Subjectivity", "Sensitivity"),
        ("Narrativity", "Accessibility"),
        ("Warmth", "Longevity"),
    ]

    # Available width for each column
    # Account for panel padding (2) and some space between columns (4)
    available_width = BOX_WIDTH - 6
    column_width = available_width // 2

    def format_single_note(metric_name: str, note: str) -> tuple[Text, int]:
        """Format a single note and return content plus line count"""
        content = Text()

        # Get the style name for this metric from the theme
        metric_style = COLOR_SCHEME.get(metric_name.lower(), "white")

        # Add metric name using the theme style
        content.append(f"{metric_name}", style=metric_style)
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

    def format_group_header(group_name: str) -> tuple[Text, int]:
        """Format a group header and return content plus line count"""
        title, _ = GROUP_HEADERS[group_name.lower()]
        content = Text()
        content.append(f"{title.upper()}", style="bold dim white")
        return content, 1  # just header line

    # Build all content rows
    all_content: list[tuple[Text, Text]] = []

    for left_item, right_item in grid_rows:
        left_content = Text()
        right_content = Text()
        left_height = 0
        right_height = 0

        # Handle group headers
        if left_item.startswith("__") and left_item.endswith("_HEADER"):
            group_name = left_item.replace("__", "").replace("_HEADER", "")
            left_content, left_height = format_group_header(group_name)
        elif left_item in notes_dict:
            left_content, left_height = format_single_note(left_item, notes_dict[left_item])

        if right_item.startswith("__") and right_item.endswith("_HEADER"):
            group_name = right_item.replace("__", "").replace("_HEADER", "")
            right_content, right_height = format_group_header(group_name)
        elif right_item in notes_dict:
            right_content, right_height = format_single_note(right_item, notes_dict[right_item])

        # Only include rows where at least one side has content
        if left_height > 0 or right_height > 0:
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

    # Create columns
    columns_display = Columns([final_left, final_right], equal=True, expand=True)

    # Add extra spacing at top
    panel_content = Group("", columns_display)

    # Create a custom box with invisible borders
    invisible_box = Box("    \n    \n    \n    \n    \n    \n    \n    \n")

    # Wrap in panel with invisible border
    notes_panel = Panel(
        panel_content,
        title="[bold white]Notes[/bold white]",
        box=invisible_box,
        padding=(0, 1),
        width=BOX_WIDTH,
        expand=False,
    )

    return notes_panel


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
            render_diamonds(left_filled_count, left_empty_count, content, left_style, reversed=True)
            content.append(f" {left_score.value}", style=left_style)
            content.append(" │ ", style="dim white")

            # Right side: number, diamonds, left-aligned name
            right_name = right_metric.title()

            content.append(f"{right_score.value} ", style=right_style)
            # Right side: filled diamonds first, then empty (normal)
            render_diamonds(
                right_filled_count, right_empty_count, content, right_style, reversed=False
            )
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

    # Center the content in the panel
    centered_content = Align.center(panel_content)

    main_panel = Panel(
        centered_content,
        title=f"[bold white]{METRICS_TITLE}[/bold white]",
        border_style="white",
        padding=(0, 1),
        width=BOX_WIDTH,
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


def format_doc_stats(doc: TextDoc, text: str) -> RenderableType:
    """
    Format document statistics in two columns using TextDoc object.
    """
    from chopdiff.docs import TextUnit
    from rich.columns import Columns

    # Calculate document statistics from doc object
    bytes_count = len(text.encode("utf-8"))
    lines = doc.size(TextUnit.lines)
    paras = doc.size(TextUnit.paragraphs)
    sents = doc.size(TextUnit.sentences)
    words = doc.size(TextUnit.words)
    tokens = doc.size(TextUnit.tiktokens)

    # Calculate responsive layout based on BOX_WIDTH
    # Account for panel borders (2), padding (2), and column separator space
    available_width = BOX_WIDTH - 6
    left_column_width = available_width // 2

    # Left column: Bytes, Lines, Tokens (labels left-aligned, numbers right-aligned)
    left_content = Text()
    bytes_str = f"{bytes_count:,}"
    left_content.append("Bytes: ", style="dim white")
    left_content.append(bytes_str.rjust(left_column_width - 7), style="bold white")
    left_content.append("\n")

    lines_str = f"{lines:,}"
    left_content.append("Lines: ", style="dim white")
    left_content.append(lines_str.rjust(left_column_width - 7), style="bold white")
    left_content.append("\n")

    tokens_str = f"{tokens:,}"
    left_content.append("Tokens: ", style="dim white")
    left_content.append(tokens_str.rjust(left_column_width - 8), style="bold white")

    # Right column: Paras, Sentences, Words (also right-aligned)
    right_column_width = available_width - left_column_width
    right_content = Text()

    paras_str = f"{paras:,}"
    right_content.append("Paras: ", style="dim white")
    right_content.append(paras_str.rjust(right_column_width - 7), style="bold white")
    right_content.append("\n")

    sents_str = f"{sents:,}"
    right_content.append("Sentences: ", style="dim white")
    right_content.append(sents_str.rjust(right_column_width - 11), style="bold white")
    right_content.append("\n")

    words_str = f"{words:,}"
    right_content.append("Words: ", style="dim white")
    right_content.append(words_str.rjust(right_column_width - 7), style="bold white")

    # Create two-column layout with responsive padding
    column_padding = max(1, (BOX_WIDTH - 50) // 10)  # More padding for wider boxes
    columns_display = Columns(
        [left_content, right_content], equal=False, expand=False, padding=(0, column_padding)
    )

    doc_panel = Panel(
        columns_display,
        title="[bold white]Size Summary[/bold white]",
        border_style="white",
        padding=(0, 1),
        width=BOX_WIDTH,
    )

    return doc_panel


def format_complete_analysis(
    prose_metrics: ProseMetrics,
    doc: TextDoc,
    text: str,
) -> RenderableType:
    """
    Format complete analysis with document stats and prose metrics.
    """
    # Create document summary panel
    doc_panel = format_doc_stats(doc, text)

    # Create metrics panel
    metrics_panel = format_prose_metrics_rich(prose_metrics)

    # Combine with spacing
    return Group(doc_panel, "", metrics_panel)


## Tests


def test_compact_format():
    """Test the complete analysis format with document stats and metrics."""
    from chopdiff.docs import TextDoc
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

    # Create test text and doc
    test_text = "This is a sample text for testing the document statistics and formatting. " * 1000
    test_doc = TextDoc.from_text(test_text)

    console = Console()
    console.print(format_complete_analysis(test_metrics, test_doc, test_text))

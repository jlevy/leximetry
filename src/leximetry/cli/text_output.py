from __future__ import annotations

from textwrap import wrap
from typing import TYPE_CHECKING, Any, cast

from chopdiff.docs import TextDoc
from rich.align import Align
from rich.box import Box
from rich.columns import Columns
from rich.console import Group, RenderableType
from rich.panel import Panel
from rich.text import Text

from leximetry.cli.rich_styles import COLOR_SCHEME, GROUP_HEADERS, LEXIMETRY_THEME

if TYPE_CHECKING:
    from leximetry.eval.metrics_model import ProseMetrics, Score

METRICS_TITLE = "Leximetry"
REPORT_WIDTH = 72

# Diamond symbols for score visualization
FILLED_DIAMOND = "◆"
EMPTY_DIAMOND = " "


def get_group_metrics(prose_metrics: ProseMetrics) -> dict[str, list[str]]:
    """Get group names and their metrics from the model structure."""
    groups: dict[str, list[str]] = {}
    model_fields = cast(dict[str, Any], type(prose_metrics).model_fields)
    for field_name in model_fields:
        group = getattr(prose_metrics, field_name)
        group_model_fields = cast(dict[str, Any], type(group).model_fields)
        metric_names = list(group_model_fields.keys())
        groups[field_name] = metric_names
    return groups


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


def collect_notes(prose_metrics: ProseMetrics) -> list[tuple[str, str]]:
    """
    Collect all notes from the prose metrics.
    """
    notes: list[tuple[str, str]] = []

    groups = get_group_metrics(prose_metrics)
    for group_name, metric_names in groups.items():
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

    # Define the horizontal pairs based on model structure
    grid_rows = [
        # Group headers for first section
        ("__EXPRESSION_HEADER", "__GROUNDEDNESS_HEADER"),
        # Expression vs Groundedness metrics
        ("Clarity", "Factuality"),
        ("Coherence", "Rigor"),
        ("Sincerity", "Depth"),
        # Group headers for second section
        ("__STYLE_HEADER", "__IMPACT_HEADER"),
        # Style vs Impact metrics
        ("Subjectivity", "Sensitivity"),
        ("Narrativity", "Accessibility"),
        ("Warmth", "Longevity"),
    ]

    # Available width for each column
    # Account for panel padding (2) and some space between columns (4)
    available_width = REPORT_WIDTH - 6
    column_width = available_width // 2

    def format_single_note(
        metric_name: str, note: str, align_right: bool = False
    ) -> tuple[Text, int]:
        """Format a single note and return content plus line count"""
        content = Text()

        # Get the style name for this metric from the theme
        metric_style = COLOR_SCHEME.get(metric_name.lower(), "white")

        # Add metric name using the theme style with alignment
        if align_right:
            content.append(f"{metric_name:>{column_width}}", style=metric_style)
        else:
            content.append(f"{metric_name}", style=metric_style)
        content.append("\n")

        # Wrap the note text
        wrapped_lines = wrap(note, width=column_width)

        for j, line in enumerate(wrapped_lines):
            if j > 0:
                content.append("\n")
            if align_right:
                content.append(f"{line:>{column_width}}", style="hint")
            else:
                content.append(line, style="hint")

        # Calculate total lines: 1 for name + 1 for newline + wrapped lines
        total_lines = 2 + len(wrapped_lines)

        return content, total_lines

    def format_group_header(group_name: str, align_right: bool = False) -> tuple[Text, int]:
        """Format a group header and return content plus line count"""
        title, _ = GROUP_HEADERS[group_name.lower()]
        content = Text()
        if align_right:
            content.append(f"{title.upper():>{column_width}}", style="category_name")
        else:
            content.append(f"{title.upper()}", style="category_name")
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
            # EXPRESSION and STYLE should be left-aligned in the left column
            left_content, left_height = format_group_header(group_name, align_right=False)
        elif left_item in notes_dict:
            left_content, left_height = format_single_note(
                left_item, notes_dict[left_item], align_right=True
            )

        if right_item.startswith("__") and right_item.endswith("_HEADER"):
            group_name = right_item.replace("__", "").replace("_HEADER", "")
            # GROUNDEDNESS and IMPACT should be right-aligned in the right column
            right_content, right_height = format_group_header(group_name, align_right=True)
        elif right_item in notes_dict:
            right_content, right_height = format_single_note(
                right_item, notes_dict[right_item], align_right=False
            )

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
        title="[panel_title]Scoring Notes[/panel_title]",
        box=invisible_box,
        padding=(0, 0),
        width=REPORT_WIDTH,
        expand=False,
    )

    return notes_panel


def format_prose_metrics_rich(prose_metrics: ProseMetrics) -> RenderableType:
    """
    Format ProseMetrics object with rich formatting matching the sample layout.
    """

    # Get all the data dynamically
    expression = prose_metrics.expression
    style = prose_metrics.style
    groundedness = prose_metrics.groundedness
    impact = prose_metrics.impact

    # Get metric names from model structure
    exp_metrics = list(type(expression).model_fields.keys())
    style_metrics = list(type(style).model_fields.keys())
    ground_metrics = list(type(groundedness).model_fields.keys())
    impact_metrics = list(type(impact).model_fields.keys())

    # Create the layout with proper spacing and labels
    content = Text()

    # Top row with group labels
    content.append("EXPRESSION", style="category_name")
    content.append("            ╭───────────╮           ", style="white")
    content.append("GROUNDEDNESS", style="category_name")
    content.append("\n")

    # Expression vs Groundedness rows
    for i in range(3):
        exp_score = getattr(expression, exp_metrics[i])
        ground_score = getattr(groundedness, ground_metrics[i])

        exp_color = COLOR_SCHEME.get(exp_metrics[i], "white")
        ground_color = COLOR_SCHEME.get(ground_metrics[i], "white")

        # Create diamond displays (right-aligned for left, left-aligned for right)
        left_diamonds = (EMPTY_DIAMOND * (5 - exp_score.value)) + (FILLED_DIAMOND * exp_score.value)
        right_diamonds = (FILLED_DIAMOND * ground_score.value) + (
            EMPTY_DIAMOND * (5 - ground_score.value)
        )

        # Format the row: right-aligned metric_name score│diamonds│diamonds│score left-aligned metric_name
        content.append(f"{exp_metrics[i].title():>18}   {exp_score.value}", style=exp_color)
        content.append("│", style="white")
        content.append(f"{left_diamonds}", style=exp_color)
        content.append("│", style="white")
        content.append(f"{right_diamonds}", style=ground_color)
        content.append("│", style="white")
        content.append(f"{ground_score.value}  {ground_metrics[i].title():<17}", style=ground_color)
        content.append("\n")

    # Separator row
    content.append("STYLE", style="category_name")
    content.append("                 │─────┼─────│                 ", style="white")
    content.append("IMPACT", style="category_name")
    content.append("\n")

    # Style vs Impact rows
    for i in range(3):
        style_score = getattr(style, style_metrics[i])
        impact_score = getattr(impact, impact_metrics[i])

        style_color = COLOR_SCHEME.get(style_metrics[i], "white")
        impact_color = COLOR_SCHEME.get(impact_metrics[i], "white")

        # Create diamond displays (right-aligned for left, left-aligned for right)
        left_diamonds = (EMPTY_DIAMOND * (5 - style_score.value)) + (
            FILLED_DIAMOND * style_score.value
        )
        right_diamonds = (FILLED_DIAMOND * impact_score.value) + (
            EMPTY_DIAMOND * (5 - impact_score.value)
        )

        # Format the row: right-aligned metric_name score│diamonds│diamonds│score left-aligned metric_name
        content.append(f"{style_metrics[i].title():>18}   {style_score.value}", style=style_color)
        content.append("│", style="white")
        content.append(f"{left_diamonds}", style=style_color)
        content.append("│", style="white")
        content.append(f"{right_diamonds}", style=impact_color)
        content.append("│", style="white")
        content.append(f"{impact_score.value}  {impact_metrics[i].title():<17}", style=impact_color)
        if i < 2:  # Don't add newline after last row
            content.append("\n")

    # Bottom row with group labels
    content.append("\n")
    content.append("                      ╰───────────╯                       ")

    main_panel = Panel(
        Align.center(content),
        title=f"[panel_title]{METRICS_TITLE}[/panel_title]",
        border_style="panel_title",
        padding=(0, 2),
        width=REPORT_WIDTH,
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

    groups = get_group_metrics(prose_metrics)
    for group_name, metric_names in groups.items():
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

    # Calculate responsive layout based on REPORT_WIDTH
    # Account for panel borders (2), padding (4), and column separator space
    available_width = REPORT_WIDTH - 8
    left_column_width = available_width // 2

    # Left column: Bytes, Lines, Tokens (labels left-aligned, numbers right-aligned)
    left_content = Text()
    bytes_str = f"{bytes_count:,}"
    left_content.append("Bytes: ", style="hint")
    left_content.append(bytes_str.rjust(left_column_width - 7), style="bold white")
    left_content.append("\n")

    lines_str = f"{lines:,}"
    left_content.append("Lines: ", style="hint")
    left_content.append(lines_str.rjust(left_column_width - 7), style="bold white")
    left_content.append("\n")

    tokens_str = f"{tokens:,}"
    left_content.append("Tokens: ", style="hint")
    left_content.append(tokens_str.rjust(left_column_width - 8), style="bold white")

    # Right column: Paras, Sentences, Words (also right-aligned)
    right_column_width = available_width - left_column_width
    right_content = Text()

    paras_str = f"{paras:,}"
    right_content.append("Paras: ", style="hint")
    right_content.append(paras_str.rjust(right_column_width - 7), style="bold white")
    right_content.append("\n")

    sents_str = f"{sents:,}"
    right_content.append("Sentences: ", style="hint")
    right_content.append(sents_str.rjust(right_column_width - 11), style="bold white")
    right_content.append("\n")

    words_str = f"{words:,}"
    right_content.append("Words: ", style="hint")
    right_content.append(words_str.rjust(right_column_width - 7), style="bold white")

    # Create two-column layout with equal columns and minimal padding
    columns_display = Columns(
        [left_content, right_content], equal=True, expand=True, padding=(0, 1)
    )

    doc_panel = Panel(
        columns_display,
        title="[panel_title]Size Summary[/panel_title]",
        border_style="panel_title",
        padding=(0, 2),
        width=REPORT_WIDTH,
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
            depth=Score(value=3, note=""),
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

    console = Console(theme=LEXIMETRY_THEME)
    console.print(format_complete_analysis(test_metrics, test_doc, test_text))

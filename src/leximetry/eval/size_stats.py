from __future__ import annotations

from datetime import timedelta

from chopdiff.docs import TextDoc, TextUnit
from prettyfmt import fmt_timedelta
from rich.columns import Columns
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text

REPORT_WIDTH = 72

WORDS_PER_PAGE = 275
WORDS_PER_MINUTE = 200


def _add_stat_line(
    content: Text, label: str, value: str, column_width: int, add_newline: bool = True
) -> None:
    """Add a formatted statistic line with right-aligned value."""
    content.append(label, style="hint")
    content.append(value.rjust(column_width - len(label)), style="bold white")
    if add_newline:
        content.append("\n")


def format_doc_stats(doc: TextDoc, text: str) -> RenderableType:
    """
    Format document statistics in two columns using TextDoc object.
    """
    # Calculate document statistics from doc object
    bytes_count = len(text.encode("utf-8"))
    lines = doc.size(TextUnit.lines)
    paras = doc.size(TextUnit.paragraphs)
    sents = doc.size(TextUnit.sentences)
    words = doc.size(TextUnit.words)
    tokens = doc.size(TextUnit.tiktokens)

    # Calculate derived statistics
    pages = max(1, round(words / WORDS_PER_PAGE))
    read_minutes = words / WORDS_PER_MINUTE
    read_time = fmt_timedelta(timedelta(minutes=read_minutes))

    # Calculate responsive layout based on REPORT_WIDTH
    # Account for panel borders (2), padding (4), and column separator space
    available_width = REPORT_WIDTH - 8
    left_column_width = available_width // 2

    # Left column: Read time, Lines, Tokens, Bytes
    left_content = Text()
    _add_stat_line(left_content, "Read time: ", read_time, left_column_width)
    _add_stat_line(left_content, "Lines: ", f"{lines:,}", left_column_width)
    _add_stat_line(left_content, "Tokens: ", f"{tokens:,}", left_column_width)
    _add_stat_line(
        left_content, "Bytes: ", f"{bytes_count:,}", left_column_width, add_newline=False
    )

    # Right column: Pages, Paras, Sentences, Words
    right_column_width = available_width - left_column_width
    right_content = Text()
    _add_stat_line(right_content, "Pages: ", f"{pages:,}", right_column_width)
    _add_stat_line(right_content, "Paragraphs: ", f"{paras:,}", right_column_width)
    _add_stat_line(right_content, "Sentences: ", f"{sents:,}", right_column_width)
    _add_stat_line(right_content, "Words: ", f"{words:,}", right_column_width, add_newline=False)

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

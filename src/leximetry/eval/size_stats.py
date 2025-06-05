from __future__ import annotations

from typing import TYPE_CHECKING

from chopdiff.docs import TextDoc, TextUnit
from rich.columns import Columns
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text

if TYPE_CHECKING:
    pass

REPORT_WIDTH = 72


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

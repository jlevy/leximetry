"""
Leximetry CLI.

For more information: https://github.com/jlevy/leximetry
"""

import argparse
import sys
from importlib.metadata import version
from pathlib import Path
from textwrap import dedent
from typing import Literal

from chopdiff.docs import TextDoc, TextUnit
from clideps.env_vars.dotenv_utils import load_dotenv_paths
from clideps.utils.readable_argparse import ReadableColorFormatter, get_readable_console_width
from rich import print as rprint
from rich.console import Console

from leximetry.cli.rich_styles import LEXIMETRY_THEME
from leximetry.cli.text_output import format_complete_analysis
from leximetry.eval.evaluate_text import evaluate_text

APP_NAME = "leximetry"

DESCRIPTION = """Leximetry: Measure your words"""


def get_version_name() -> str:
    """Get formatted version string"""
    try:
        leximetry_version = version(APP_NAME)
        return f"{APP_NAME} v{leximetry_version}"
    except Exception:
        return "(unknown version)"


def build_parser() -> argparse.ArgumentParser:
    """Build the main argument parser"""
    parser = argparse.ArgumentParser(
        formatter_class=ReadableColorFormatter,
        epilog=dedent((__doc__ or "") + "\n\n" + get_version_name()),
        description=DESCRIPTION,
    )
    parser.add_argument("--version", action="version", version=get_version_name())
    parser.add_argument(
        "--debug", action="store_true", help="enable debug logging (log level: debug)"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="enable verbose logging (log level: info)"
    )
    parser.add_argument("--quiet", action="store_true", help="only log errors (log level: error)")
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-4o",
        help="Model to use for evaluation. Examples: gpt-4o-mini, gpt-4o, claude-4-sonnet-latest, claude-3-haiku-latest, gemini-2.0-flash",
    )
    parser.add_argument(
        "--save",
        type=str,
        help="Save output to the specified file in JSON instead of printing to console",
    )
    parser.add_argument("input", type=str, help="Path to the input text file")

    return parser


def get_log_level(args: argparse.Namespace) -> Literal["debug", "info", "warning", "error"]:
    """Get log level from command line arguments"""
    if args.quiet:
        return "error"
    elif args.verbose:
        return "info"
    elif args.debug:
        return "debug"
    else:
        return "warning"


def main() -> None:
    """
    Main entry point for the CLI.
    """
    # Create console with our theme
    console = Console(theme=LEXIMETRY_THEME, width=get_readable_console_width())

    parser = build_parser()
    args = parser.parse_args()

    try:
        load_dotenv_paths()
        text = Path(args.input).read_text()

        # Calculate document statistics
        doc = TextDoc.from_text(text)
        bytes_count = len(text.encode("utf-8"))
        lines = doc.size(TextUnit.lines)
        paras = doc.size(TextUnit.paragraphs)
        sents = doc.size(TextUnit.sentences)
        words = doc.size(TextUnit.words)
        tokens = doc.size(TextUnit.tiktokens)

        result = evaluate_text(text, args.model)

        if args.save:
            # Save to JSON file
            output_path = Path(args.save)
            output_path.write_text(result.model_dump_json(indent=2))
            rprint(f"[green]Results saved to {output_path}[/green]")
        else:
            # Print with rich formatting including document stats
            console.print(
                format_complete_analysis(
                    result,
                    bytes_count=bytes_count,
                    lines=lines,
                    paras=paras,
                    sents=sents,
                    words=words,
                    tokens=tokens,
                )
            )

    except FileNotFoundError as e:
        rprint(f"[red]File not found: {e}[/red]")
        sys.exit(1)
    except KeyboardInterrupt:
        rprint()
        rprint("[yellow]Cancelled[/yellow]")
        sys.exit(130)
    except Exception as e:
        rprint(f"[red]Error: {e}[/red]")
        if get_log_level(args) == "debug":
            import traceback

            traceback.print_exc()
        sys.exit(2)


if __name__ == "__main__":
    main()

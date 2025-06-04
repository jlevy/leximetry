"""
Script to update README.md with content from leximetry.md.

This script reads the content from leximetry.md and replaces the content
in README.md between the BEGIN INCLUDE and END INCLUDE markers.
"""

from __future__ import annotations

from pathlib import Path


def update_readme() -> None:
    """Update README.md with content from leximetry.md."""
    # Get paths relative to this script's location
    script_dir = Path(__file__).parent
    leximetry_md_path = script_dir / "leximetry.md"
    readme_path = script_dir.parent.parent.parent / "README.md"

    # Read the source content
    if not leximetry_md_path.exists():
        raise FileNotFoundError(f"Source file not found: {leximetry_md_path}")

    leximetry_content = leximetry_md_path.read_text(encoding="utf-8")

    # Read the current README
    if not readme_path.exists():
        raise FileNotFoundError(f"README file not found: {readme_path}")

    readme_content = readme_path.read_text(encoding="utf-8")

    # Find the include markers
    begin_marker = "<!-- BEGIN INCLUDE: leximetry.md -->"
    end_marker = "<!-- END INCLUDE: leximetry.md -->"

    begin_pos = readme_content.find(begin_marker)
    end_pos = readme_content.find(end_marker)

    if begin_pos == -1:
        raise ValueError(f"Begin marker not found: {begin_marker}")
    if end_pos == -1:
        raise ValueError(f"End marker not found: {end_marker}")
    if end_pos <= begin_pos:
        raise ValueError("End marker appears before begin marker")

    # Replace the content between markers
    before_content = readme_content[: begin_pos + len(begin_marker)]
    after_content = readme_content[end_pos:]

    # Construct the new README content
    new_readme_content = f"{before_content}\n\n{leximetry_content}\n\n{after_content}"

    # Write the updated README
    readme_path.write_text(new_readme_content, encoding="utf-8")

    print(f"Successfully updated {readme_path} with content from {leximetry_md_path}")


if __name__ == "__main__":
    update_readme()

"""
Rich styling and color definitions for Leximetry CLI.
"""

from colour import Color
from rich.theme import Theme


def hsl_to_hex(hsl_string: str) -> str:
    """
    Convert an HSL/HSLA string to an RGB hex string or RGBA value.
    "hsl(134, 43%, 60%)" -> "#6dbd6d"
    "hsla(220, 14%, 96%, 0.86)" -> "rgba(244, 245, 247, 0.86)"
    """
    is_hsla = hsl_string.startswith("hsla")
    hsl_values = (
        hsl_string.replace("hsla(", "")
        .replace("hsl(", "")
        .replace(")", "")
        .replace("%", "")
        .split(",")
    )

    if is_hsla:
        hue, saturation, lightness, alpha = (float(value.strip()) for value in hsl_values)
    else:
        hue, saturation, lightness = (float(value.strip()) for value in hsl_values)
        alpha = 1.0

    saturation /= 100
    lightness /= 100

    color = Color(hsl=(hue / 360, saturation, lightness))

    if alpha < 1:
        rgb: tuple[float, float, float] = color.rgb  # pyright: ignore
        return f"rgba({int(rgb[0] * 255)}, {int(rgb[1] * 255)}, {int(rgb[2] * 255)}, {alpha})"
    return color.hex_l


# Define theme with named styles for each metric
LEXIMETRY_THEME = Theme(
    {
        # Expression group - Yellow/green tones
        "clarity": f"bold {hsl_to_hex('hsl(75, 71%, 71%)')}",
        "coherence": f"bold {hsl_to_hex('hsl(55, 80%, 63%)')}",
        "sincerity": f"bold {hsl_to_hex('hsl(25, 80%, 65%)')}",
        # Style group - Purple/pink tones
        "narrativity": f"bold {hsl_to_hex('hsl(270, 63%, 73%)')}",
        "subjectivity": f"bold {hsl_to_hex('hsl(290, 54%, 65%)')}",
        "warmth": f"bold {hsl_to_hex('hsl(320, 70%, 65%)')}",
        # Groundedness group - Blue tones
        "factuality": f"bold {hsl_to_hex('hsl(229, 66%, 65%)')}",
        "rigor": f"bold {hsl_to_hex('hsl(248, 75%, 68%)')}",
        "thoroughness": f"bold {hsl_to_hex('hsl(218, 57%, 80%)')}",
        # Impact group - Mixed colors
        "accessibility": f"bold {hsl_to_hex('hsl(188, 44%, 62%)')}",
        "longevity": f"bold {hsl_to_hex('hsl(117, 23%, 59%)')}",
        "sensitivity": f"bold {hsl_to_hex('hsl(0, 69%, 63%)')}",
        # Utility styles
        "metric_name": "dim",
        "header": "bold dim white",
        "separator": "dim white",
    }
)

# Color scheme mapping to theme style names
COLOR_SCHEME = {
    "clarity": "clarity",
    "coherence": "coherence",
    "sincerity": "sincerity",
    "narrativity": "narrativity",
    "subjectivity": "subjectivity",
    "warmth": "warmth",
    "factuality": "factuality",
    "rigor": "rigor",
    "thoroughness": "thoroughness",
    "accessibility": "accessibility",
    "longevity": "longevity",
    "sensitivity": "sensitivity",
}

# Group headers with their display names and colors
GROUP_HEADERS: dict[str, tuple[str, str]] = {
    "expression": ("Expression", "white"),
    "style": ("Style", "white"),
    "groundedness": ("Groundedness", "white"),
    "impact": ("Impact", "white"),
}

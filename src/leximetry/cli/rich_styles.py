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
        "clarity": f"bold {hsl_to_hex('hsl(80, 71%, 70%)')}",
        "coherence": f"bold {hsl_to_hex('hsl(55, 80%, 70%)')}",
        "sincerity": f"bold {hsl_to_hex('hsl(25, 80%, 70%)')}",
        # Style group - Purple/pink tones
        "subjectivity": f"bold {hsl_to_hex('hsl(260, 54%, 73%)')}",
        "narrativity": f"bold {hsl_to_hex('hsl(295, 63%, 73%)')}",
        "warmth": f"bold {hsl_to_hex('hsl(340, 60%, 73%)')}",
        # Groundedness group - Blue tones
        "factuality": f"bold {hsl_to_hex('hsl(230, 53%, 70%)')}",
        "thoroughness": f"bold {hsl_to_hex('hsl(200, 50%, 70%)')}",
        "rigor": f"bold {hsl_to_hex(hsl_string='hsl(185, 38%, 50%)')}",
        # Impact group - Mixed colors
        "sensitivity": f"bold {hsl_to_hex('hsl(0, 39%, 60%)')}",
        "accessibility": f"bold {hsl_to_hex('hsl(60, 34%, 70%)')}",
        "longevity": f"bold {hsl_to_hex('hsl(90, 33%, 50%)')}",
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
    "subjectivity": "subjectivity",
    "narrativity": "narrativity",
    "warmth": "warmth",
    "factuality": "factuality",
    "thoroughness": "thoroughness",
    "rigor": "rigor",
    "sensitivity": "sensitivity",
    "accessibility": "accessibility",
    "longevity": "longevity",
}

# Group headers with their display names and colors
GROUP_HEADERS: dict[str, tuple[str, str]] = {
    "expression": ("Expression", "white"),
    "style": ("Style", "white"),
    "groundedness": ("Groundedness", "white"),
    "impact": ("Impact", "white"),
}

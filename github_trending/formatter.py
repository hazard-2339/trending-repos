"""Human-readable output formatting."""

from collections.abc import Iterable
from typing import Any


OSC8_START = "\033]8;;"
OSC8_END = "\033\\"


def terminal_link(label: str, url: str | None) -> str:
    """Wrap a label in an OSC 8 terminal hyperlink when a URL is available."""
    if not url:
        return label
    return f"{OSC8_START}{url}{OSC8_END}{label}{OSC8_START}{OSC8_END}"


def format_repositories(repositories: Iterable[dict[str, Any]]) -> str:
    """Format repository records as a compact text table."""
    lines = []
    for index, repository in enumerate(repositories, start=1):
        # GitHub normally supplies full_name, but the fallback keeps formatting
        # useful for partial records and makes the function easier to reuse.
        name = repository.get("full_name", repository.get("name", "unknown"))
        # GitHub includes html_url in each repository result. OSC 8 keeps the
        # visible output unchanged while allowing compatible terminals to open
        # the repository when its name is clicked.
        name = terminal_link(name, repository.get("html_url"))
        stars = repository.get("stargazers_count", 0)
        # Descriptions may contain line breaks; flatten them so each repository
        # remains visually grouped under its numbered result.
        description = (repository.get("description") or "").replace("\n", " ").strip()
        lines.append(f"{index:>2}. {name} ({stars:,} stars)")
        if description:
            lines.append(f"    {description}")

    # An explicit empty-state message is clearer than printing a blank terminal.
    return "\n".join(lines) if lines else "No repositories found."

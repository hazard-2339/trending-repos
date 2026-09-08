"""Date range helpers for GitHub repository searches."""

from datetime import date, timedelta


def date_range(days: int, end: date | None = None) -> tuple[date, date]:
    """Return an inclusive UTC date range ending today or at ``end``."""
    if days < 1:
        raise ValueError("days must be at least 1")

    # ``days - 1`` makes both endpoints inclusive: a one-day search starts and
    # ends on the same date rather than accidentally covering two dates.
    end_date = end or date.today()
    return end_date - timedelta(days=days - 1), end_date


def github_query(days: int, end: date | None = None) -> str:
    """Build the GitHub search qualifier for repositories created recently."""
    start, end_date = date_range(days, end)
    return f"created:{start.isoformat()}..{end_date.isoformat()}"

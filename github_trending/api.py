"""Small client for the public GitHub Search API."""

import json
from collections.abc import Callable
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_URL = "https://api.github.com/search/repositories"


class GitHubAPIError(RuntimeError):
    """Raised when GitHub returns an unsuccessful response."""


def search_repositories(
    query: str,
    *,
    language: str | None = None,
    limit: int = 10,
    opener: Callable[..., Any] = urlopen,
) -> list[dict[str, Any]]:
    """Search repositories and return at most ``limit`` result items."""
    if limit < 1:
        raise ValueError("limit must be at least 1")

    # GitHub accepts search qualifiers as one query string. Add the optional
    # language qualifier only when the user supplied one.
    qualifiers = query
    if language:
        qualifiers = f"{qualifiers} language:{language}"

    # urlencode handles spaces and punctuation safely instead of building a URL
    # with string concatenation.
    params = urlencode({"q": qualifiers, "sort": "stars", "order": "desc", "per_page": limit})
    request = Request(
        f"{API_URL}?{params}",
        headers={"Accept": "application/vnd.github+json", "User-Agent": "github-trending"},
    )

    try:
        # The context manager closes the response even when JSON parsing fails.
        with opener(request, timeout=15) as response:
            payload = json.load(response)
    except Exception as exc:
        raise GitHubAPIError(f"GitHub request failed: {exc}") from exc

    # A valid search response must contain an items list. Checking the shape here
    # prevents confusing errors later in the formatter.
    if not isinstance(payload, dict) or not isinstance(payload.get("items"), list):
        raise GitHubAPIError("GitHub returned an unexpected response")

    return payload["items"][:limit]

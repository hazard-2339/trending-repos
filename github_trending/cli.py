"""Command-line entry point."""

import argparse

from .api import GitHubAPIError, search_repositories
from .config import load_defaults
from .formatter import format_repositories
from .utils import github_query


def build_parser() -> argparse.ArgumentParser:
    # Keeping argument definitions in one parser makes the command self-documenting:
    # argparse automatically provides --help and validates typed values for us.
    parser = argparse.ArgumentParser(description="Find recently created popular GitHub repositories.")
    defaults = load_defaults()
    parser.add_argument(
        "--days", type=int, default=defaults.get("days", 7), help="Number of days to search (default: %(default)s)."
    )
    parser.add_argument(
        "--language", default=defaults.get("language"), help="Filter results by programming language (default: %(default)s)."
    )
    parser.add_argument(
        "--limit", type=int, default=defaults.get("limit", 10), help="Maximum repositories to show (default: %(default)s)."
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        # Convert the user's date-window option into GitHub's search syntax before
        # calling the API. The API function remains reusable outside the CLI.
        repositories = search_repositories(
            github_query(args.days), language=args.language, limit=args.limit
        )
    except (GitHubAPIError, ValueError) as exc:
        # Return a friendly command-line error instead of exposing a traceback for
        # expected input errors or network/API failures.
        print(f"Error: {exc}")
        return 1

    # Formatting is deliberately separate from fetching so output can change
    # without changing the API client.
    print(format_repositories(repositories))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

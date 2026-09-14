# github-trending

A command-line tool that finds recently created, popular GitHub repositories
using the public GitHub REST API — no authentication required.

> **Note:** GitHub doesn't expose a public API for its website's "Trending"
> page. This tool approximates it by searching for repositories **created**
> within a chosen time window, sorted by star count — the same technique
> used by most open-source "trending" CLIs.

## Features

- Search repositories created within the last N days.
- Optional filter by programming language.
- Control how many results are shown typee shii.
- Clickable repository links in supporting terminals.
- Clear error handling for network issues, rate limits, and invalid input.

## Installation

### Requirements
- Python 3.9+
- pip

### Setup

```bash
git clone https://github.com/<your-username>/trending-repos.git
cd trending-repos

python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS/Linux
source .venv/bin/activate

pip install -e .
```

## Usage

```bash
python -m github_trending.cli [--days DAYS] [--language LANGUAGE] [--limit LIMIT]
```

Save defaults in `~/.trending-reposrc` to avoid repeating common options:

```ini
[defaults]
days = 30
language = Python
limit = 20
```

Command-line options override values saved in the config file.

The tool uses GitHub's public repository search API. Unauthenticated requests are subject to GitHub's rate limits.

| Flag           | Description                                    | Default |
|----------------|-------------------------------------------------|---------|
| `--days`       | Number of days back to search                   | `7`     |
| `--language`   | Filter results by programming language           | none    |
| `--limit`      | Maximum number of repositories to display        | `10`    |
| `-h, --help`   | Show help message                                |         |

### Examples

```bash
# Default: repos created in the last 7 days, top 10 results
python -m github_trending.cli

# Repos created in the last 30 days, top 20 results
python -m github_trending.cli --days 30 --limit 20

# Filter by language
python -m github_trending.cli --days 30 --limit 20 --language Python
```

### Sample output

```
 1. octocat/hello-world (4,870 stars)
    A test repository showcasing GitHub features.
 2. octocat/another-repo (2,475 stars)
    Reference blueprint for building agents.
```

Repository names render as clickable links in terminals that support ANSI
hyperlinks (Windows Terminal, VS Code, iTerm2, most Linux terminals).

## Rate limits

This tool makes unauthenticated requests to the GitHub Search API, which is
capped at **10 requests per minute**. If you hit the limit, wait a minute
and try again.

## Project structure

```
trending-repos/
├── github_trending/
│   ├── __init__.py
│   ├── cli.py          # argparse entrypoint
│   ├── api.py          # GitHub API client + error handling
│   ├── formatter.py    # output formatting
│   └── utils.py        # query-building helpers
├── tests/
├── requirements.txt
├── setup.py
└── README.md
```

## Running tests

```bash
pip install pytest
pytest tests/
```

## License

MIT

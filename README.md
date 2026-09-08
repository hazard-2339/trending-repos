# GitHub Trending

A small command-line tool for finding recently created, popular GitHub repositories.

## Install

```text
python -m pip install -r requirements.txt
python -m pip install -e .
```

## Usage

```text
github-trending
github-trending --days 30 --language Python --limit 20
```

The tool uses GitHub's public repository search API. Unauthenticated requests are subject to GitHub's rate limits.

Repository names are emitted as clickable ANSI OSC 8 hyperlinks in terminals that support OSC 8.

## Tests

```text
pytest
```

"""Load saved command-line defaults."""

from configparser import ConfigParser
from pathlib import Path

CONFIG_PATH = Path.home() / ".trending-reposrc"


def load_defaults(path: Path = CONFIG_PATH) -> dict[str, str]:
    """Return supported defaults from an optional user config file."""
    if not path.is_file():
        return {}

    parser = ConfigParser()
    parser.read(path)
    if not parser.has_section("defaults"):
        return {}

    supported = {"days", "language", "limit"}
    return {key: value for key, value in parser["defaults"].items() if key in supported}
from github_trending import cli
from github_trending.config import load_defaults


def test_load_defaults_reads_supported_values(tmp_path):
    config_path = tmp_path / ".trending-reposrc"
    config_path.write_text("[defaults]\ndays = 30\nlanguage = Python\nlimit = 20\nunknown = ignored\n")

    assert load_defaults(config_path) == {"days": "30", "language": "Python", "limit": "20"}


def test_parser_uses_config_defaults_and_cli_overrides(monkeypatch, tmp_path):
    config_path = tmp_path / ".trending-reposrc"
    config_path.write_text("[defaults]\ndays = 30\nlanguage = Python\nlimit = 20\n")
    monkeypatch.setattr(cli, "load_defaults", lambda: load_defaults(config_path))
    monkeypatch.setattr("sys.argv", ["github-trending", "--limit", "5"])

    args = cli.build_parser().parse_args()

    assert args.days == 30
    assert args.language == "Python"
    assert args.limit == 5
from github_trending.formatter import format_repositories


def test_format_repositories_adds_osc8_link_without_changing_visible_name():
    output = format_repositories(
        [
            {
                "full_name": "octocat/Hello-World",
                "html_url": "https://github.com/octocat/Hello-World",
                "stargazers_count": 42,
            }
        ]
    )

    assert output == (
        " 1. \033]8;;https://github.com/octocat/Hello-World\033\\"
        "octocat/Hello-World\033]8;;\033\\ (42 stars)"
    )


def test_format_repositories_keeps_records_without_urls_plain():
    output = format_repositories([{"full_name": "example/repo"}])

    assert output == " 1. example/repo (0 stars)"
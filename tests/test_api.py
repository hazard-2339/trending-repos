import io
import json

import pytest

from github_trending.api import GitHubAPIError, search_repositories


class FakeResponse:
    # This small response double implements only the interface used by the API
    # client, so tests never make a real network request.
    def __init__(self, payload):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return json.dumps(self.payload).encode()


def test_search_repositories_builds_query_and_limits_results():
    requests = []

    def opener(request, timeout):
        requests.append((request, timeout))
        return FakeResponse({"items": [{"full_name": "example/repo"}, {"full_name": "other/repo"}]})

    # Injecting the opener lets the test inspect the generated request while
    # returning predictable GitHub data.
    repositories = search_repositories("created:2026-09-01..2026-09-07", language="Python", limit=1, opener=opener)

    assert repositories == [{"full_name": "example/repo"}]
    assert "language%3APython" in requests[0][0].full_url
    assert requests[0][1] == 15


def test_search_repositories_rejects_invalid_payload():
    def opener(request, timeout):
        return FakeResponse({"message": "bad request"})

    with pytest.raises(GitHubAPIError, match="unexpected response"):
        search_repositories("created:2026-09-01", opener=opener)

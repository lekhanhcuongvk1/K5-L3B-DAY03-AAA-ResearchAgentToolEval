"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest
import requests

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    # Call clarify with response_type="choice" and 2 options.
    # Assert: options are returned unchanged, awaiting_user is True.
    pytest.skip(TODO)


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    # Items with section "A", "B", "A" -> markdown has exactly one "## A" and one "## B".
    pytest.skip(TODO)


def test_format_thread_numbers_items() -> None:
    # template="thread" -> lines start with "1/", "2/", ...
    pytest.skip(TODO)


def test_format_empty_items_does_not_crash() -> None:
    # items=None and items=[] -> item_count == 0, no exception.
    pytest.skip(TODO)


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    # Set TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID, mock HTTP.
    # Assert: exactly one POST, URL contains the token, json has chat_id + text, status == "sent".
    pytest.skip(TODO)


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    pytest.skip(TODO)


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    # timeframe=None -> request body has no "time_range" key.
    pytest.skip(TODO)


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    # Mock {"data": {"markdown": "...", "metadata": {"title": "T", "sourceURL": "https://..."}}}
    # Assert title/url/source/summary in result["items"][0].
    pytest.skip(TODO)


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    pytest.skip(TODO)


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    # Mock {"timeline": [...]} with 1 item missing tweet_id and 6 valid items, limit=3.
    # Assert 3 items, and each url looks like https://x.com/<handle>/status/<id>.
    pytest.skip(TODO)


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    # Assert the request params carry the query and search_type ("Top" / "Latest").
    pytest.skip(TODO)


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    pytest.skip(TODO)


def test_policy_area_filter_only_returns_that_area() -> None:
    # policy_area="data_privacy" -> every result has policy_area == "data_privacy".
    pytest.skip(TODO)


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    # One policy file contains a quoted line that tries to give the assistant orders.
    # Query that section (source_citation) and assert: that line is in untrusted_text, NOT in facts.
    pytest.skip(TODO)


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

@pytest.mark.parametrize("doi", [
    "10.1234/example", " 10.1234/example ", "doi: 10.1234/example",
    "https://doi.org/10.1234/example", "http://dx.doi.org/10.1234/example",
])
def test_doi_lookup_sends_encoded_request_and_maps_metadata(doi, fake_http) -> None:
    calls = fake_http(FakeResponse({"message": {
        "DOI": "10.1234/example", "title": ["Research example"],
        "author": [{"given": "An", "family": "Nguyen"}, {"name": "Research Group"}],
        "publisher": "Example Publisher", "published": {"date-parts": [[2024, 3, 1]]},
    }}))

    result = TOOL_FUNCTIONS["doi_lookup"](doi=doi)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == "https://api.crossref.org/works/10.1234%2Fexample"
    assert calls[0]["headers"]["Accept"] == "application/json"
    assert "doi_lookup" in calls[0]["headers"]["User-Agent"]
    assert calls[0]["timeout"] == 30
    assert result == {"tool": "doi_lookup", "doi": "10.1234/example", "items": [{
        "doi": "10.1234/example", "title": "Research example",
        "authors": ["An Nguyen", "Research Group"], "publisher": "Example Publisher",
        "year": 2024, "url": "https://doi.org/10.1234/example", "source": "crossref.org",
    }]}


@pytest.mark.parametrize("doi", ["", "  ", None, 123, {}, [], "not-a-doi", "10.1234/", "https://example.com/paper"])
def test_doi_lookup_bad_input_returns_error_without_network(doi, fake_http) -> None:
    calls = fake_http(FakeResponse())

    result = TOOL_FUNCTIONS["doi_lookup"](doi=doi)

    assert result["tool"] == "doi_lookup"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert calls == []


@pytest.mark.parametrize("status_code", [404, 429, 500])
def test_doi_lookup_http_failure_returns_error_dict(status_code, fake_http) -> None:
    calls = fake_http(FakeResponse(status_code=status_code))

    result = TOOL_FUNCTIONS["doi_lookup"](doi="10.1234/example")

    assert len(calls) == 1
    assert result == {"tool": "doi_lookup", "error": "HTTPError", "message": f"HTTP {status_code}"}


@pytest.mark.parametrize("exc", [requests.Timeout("timed out"), requests.ConnectionError("offline")])
def test_doi_lookup_network_failure_returns_error_dict(exc, fake_http) -> None:
    calls = fake_http(exc)

    result = TOOL_FUNCTIONS["doi_lookup"](doi="10.1234/example")

    assert len(calls) == 1
    assert result == {"tool": "doi_lookup", "error": type(exc).__name__, "message": str(exc)}


@pytest.mark.parametrize("payload", [
    [], {}, {"message": []}, {"message": {}},
    {"message": {"DOI": "10.1234/another"}},
    {"message": {"DOI": "10.1234/example", "title": "not a list"}},
])
def test_doi_lookup_malformed_response_returns_error_dict(payload, fake_http) -> None:
    calls = fake_http(FakeResponse(payload))

    result = TOOL_FUNCTIONS["doi_lookup"](doi="10.1234/example")

    assert len(calls) == 1
    assert result["tool"] == "doi_lookup"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert "items" not in result


def test_doi_lookup_missing_optional_metadata_returns_empty_fields(fake_http) -> None:
    fake_http(FakeResponse({"message": {"DOI": "10.1234/example"}}))

    result = TOOL_FUNCTIONS["doi_lookup"](doi="10.1234/example")

    assert result["items"] == [{
        "doi": "10.1234/example", "title": "", "authors": [], "publisher": "", "year": None,
        "url": "https://doi.org/10.1234/example", "source": "crossref.org",
    }]


def test_doi_lookup_encodes_reserved_characters_in_doi(fake_http) -> None:
    calls = fake_http(FakeResponse({"message": {"DOI": "10.1234/a?b#c"}}))

    result = TOOL_FUNCTIONS["doi_lookup"](doi="https://doi.org/10.1234/a%3Fb%23c")

    assert calls[0]["url"] == "https://api.crossref.org/works/10.1234%2Fa%3Fb%23c"
    assert result["items"][0]["url"] == "https://doi.org/10.1234/a%3Fb%23c"


# ---------------- wiki_summary ----------------

def _wiki_payload(extract: str = "RAG is a technique.") -> dict:
    return {"query": {"pages": [{
        "pageid": 1, "title": "Retrieval-augmented generation", "index": 1,
        "extract": extract, "fullurl": "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
    }]}}


@pytest.mark.parametrize("lang,expected_lang", [("en", "en"), ("vi", "vi"), (" VI ", "vi")])
def test_wiki_summary_sends_search_request_and_maps_page(lang, expected_lang, fake_http) -> None:
    calls = fake_http(FakeResponse(_wiki_payload()))

    result = TOOL_FUNCTIONS["wiki_summary"](query="  retrieval augmented generation ", lang=lang)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == f"https://{expected_lang}.wikipedia.org/w/api.php"
    params = calls[0]["params"]
    assert params["gsrsearch"] == "retrieval augmented generation"
    assert params["generator"] == "search" and params["gsrlimit"] == "1"
    assert params["exintro"] == "1" and params["explaintext"] == "1"
    assert "wiki_summary" in calls[0]["headers"]["User-Agent"]
    assert calls[0]["timeout"] == 30
    assert result == {"tool": "wiki_summary", "query": "retrieval augmented generation", "lang": expected_lang, "items": [{
        "title": "Retrieval-augmented generation",
        "url": "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "source": f"{expected_lang}.wikipedia.org",
        "summary": "RAG is a technique.",
    }]}


@pytest.mark.parametrize("query,lang", [("", "en"), ("   ", "en"), (None, "en"), (123, "en"), (["RAG"], "en"),
                                        ("RAG", "fr"), ("RAG", ""), ("RAG", None)])
def test_wiki_summary_bad_input_returns_error_without_network(query, lang, fake_http) -> None:
    calls = fake_http(FakeResponse(_wiki_payload()))

    result = TOOL_FUNCTIONS["wiki_summary"](query=query, lang=lang)

    assert result["tool"] == "wiki_summary"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert calls == []


@pytest.mark.parametrize("failure,expected", [
    (FakeResponse(status_code=404), ("HTTPError", "HTTP 404")),
    (FakeResponse(status_code=429), ("HTTPError", "HTTP 429")),
    (FakeResponse(status_code=503), ("HTTPError", "HTTP 503")),
    (requests.Timeout("timed out"), ("Timeout", "timed out")),
    (requests.ConnectionError("offline"), ("ConnectionError", "offline")),
])
def test_wiki_summary_http_or_network_failure_returns_error_dict(failure, expected, fake_http) -> None:
    calls = fake_http(failure)

    result = TOOL_FUNCTIONS["wiki_summary"](query="RAG")

    assert len(calls) == 1
    assert result == {"tool": "wiki_summary", "error": expected[0], "message": expected[1]}


def test_wiki_summary_no_search_hit_returns_empty_items(fake_http) -> None:
    fake_http(FakeResponse({"batchcomplete": True}))

    result = TOOL_FUNCTIONS["wiki_summary"](query="zzqxw-nonexistent-term")

    assert result == {"tool": "wiki_summary", "query": "zzqxw-nonexistent-term", "lang": "en", "items": []}


@pytest.mark.parametrize("payload", [[], {"query": {}}, {"query": {"pages": {}}}, {"query": {"pages": [{"extract": "x"}]}}])
def test_wiki_summary_malformed_response_returns_error_dict(payload, fake_http) -> None:
    fake_http(FakeResponse(payload))

    result = TOOL_FUNCTIONS["wiki_summary"](query="RAG")

    assert result["tool"] == "wiki_summary"
    assert result["error"] == "ValueError"
    assert "items" not in result


def test_wiki_summary_truncates_long_extract(fake_http) -> None:
    fake_http(FakeResponse(_wiki_payload(extract="x" * 5000)))

    summary = TOOL_FUNCTIONS["wiki_summary"](query="RAG")["items"][0]["summary"]

    assert len(summary) == 1500
    assert summary.endswith("...")


# ---------------- hn_search ----------------

def _hn_payload() -> dict:
    return {"hits": [
        {"objectID": "101", "title": "Rust 2.0 released", "url": "https://blog.rust-lang.org/x",
         "author": "alice", "points": 512, "num_comments": 230, "created_at": "2026-11-01T10:00:00Z"},
        {"objectID": "102", "title": "Ask HN: Learning Rust?", "url": None,
         "author": "bob", "points": None, "num_comments": None, "created_at": "2026-11-02T10:00:00Z"},
        {"objectID": "", "title": "missing id is skipped"},
        {"objectID": "104", "title": None},
    ]}


@pytest.mark.parametrize("sort,endpoint", [
    ("relevance", "https://hn.algolia.com/api/v1/search"),
    ("date", "https://hn.algolia.com/api/v1/search_by_date"),
    (" DATE ", "https://hn.algolia.com/api/v1/search_by_date"),
])
def test_hn_search_uses_endpoint_for_sort_and_maps_stories(sort, endpoint, fake_http) -> None:
    calls = fake_http(FakeResponse(_hn_payload()))

    result = TOOL_FUNCTIONS["hn_search"](query=" Rust ", sort=sort, limit=3)

    assert len(calls) == 1
    assert calls[0]["method"] == "GET"
    assert calls[0]["url"] == endpoint
    assert calls[0]["params"] == {"query": "Rust", "tags": "story", "hitsPerPage": 3}
    assert calls[0]["timeout"] == 30
    assert result["tool"] == "hn_search" and result["query"] == "Rust"
    assert [item["title"] for item in result["items"]] == ["Rust 2.0 released", "Ask HN: Learning Rust?"]
    first, ask = result["items"]
    assert first["url"] == "https://blog.rust-lang.org/x"
    assert first["discussion_url"] == "https://news.ycombinator.com/item?id=101"
    assert first["metrics"] == {"points": 512, "comments": 230}
    assert first["summary"] == "512 points, 230 comments, by alice"
    # Ask HN has no external url -> falls back to the discussion link; missing metrics become 0.
    assert ask["url"] == "https://news.ycombinator.com/item?id=102"
    assert ask["metrics"] == {"points": 0, "comments": 0}


def test_hn_search_accepts_numeric_string_limit(fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    result = TOOL_FUNCTIONS["hn_search"](query="Rust", limit="7")

    assert calls[0]["params"]["hitsPerPage"] == 7
    assert result["items"] == []


@pytest.mark.parametrize("kwargs", [
    {"query": ""}, {"query": "  "}, {"query": None}, {"query": 42},
    {"query": "Rust", "sort": "top"}, {"query": "Rust", "sort": None},
    {"query": "Rust", "limit": 0}, {"query": "Rust", "limit": -1}, {"query": "Rust", "limit": 21},
    {"query": "Rust", "limit": True}, {"query": "Rust", "limit": "abc"}, {"query": "Rust", "limit": 2.5},
])
def test_hn_search_bad_input_returns_error_without_network(kwargs, fake_http) -> None:
    calls = fake_http(FakeResponse({"hits": []}))

    result = TOOL_FUNCTIONS["hn_search"](**kwargs)

    assert result["tool"] == "hn_search"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert calls == []


@pytest.mark.parametrize("failure,expected", [
    (FakeResponse(status_code=429), ("HTTPError", "HTTP 429")),
    (FakeResponse(status_code=500), ("HTTPError", "HTTP 500")),
    (requests.Timeout("timed out"), ("Timeout", "timed out")),
    (requests.ConnectionError("offline"), ("ConnectionError", "offline")),
])
def test_hn_search_http_or_network_failure_returns_error_dict(failure, expected, fake_http) -> None:
    calls = fake_http(failure)

    result = TOOL_FUNCTIONS["hn_search"](query="Rust")

    assert len(calls) == 1
    assert result == {"tool": "hn_search", "error": expected[0], "message": expected[1]}


@pytest.mark.parametrize("payload", [[], {}, {"hits": "not a list"}])
def test_hn_search_malformed_response_returns_error_dict(payload, fake_http) -> None:
    fake_http(FakeResponse(payload))

    result = TOOL_FUNCTIONS["hn_search"](query="Rust")

    assert result["tool"] == "hn_search"
    assert result["error"] == "ValueError"
    assert "items" not in result


# ---------------- github_repo ----------------
# github_repo makes two requests (repo + latest release), so these tests route by URL
# instead of using the single-response `fake_http` fixture. Still fully offline.

REPO_URL = "https://api.github.com/repos/huggingface/transformers"
REPO_PAYLOAD = {
    "full_name": "huggingface/transformers", "html_url": "https://github.com/huggingface/transformers",
    "description": "Transformers library", "language": "Python", "license": {"spdx_id": "Apache-2.0"},
    "pushed_at": "2026-11-09T12:00:00Z", "archived": False,
    "stargazers_count": 150000, "forks_count": 30000, "open_issues_count": 1200,
}
RELEASE_PAYLOAD = {"tag_name": "v5.0.0", "name": "v5.0.0", "published_at": "2026-11-01T00:00:00Z",
                   "html_url": "https://github.com/huggingface/transformers/releases/tag/v5.0.0"}


@pytest.fixture
def github_http(monkeypatch):
    def _install(routes: dict):
        calls: list[dict] = []

        def _get(url, **kwargs):
            calls.append({"url": url, **kwargs})
            response = routes[url]
            if isinstance(response, Exception):
                raise response
            return response

        monkeypatch.setattr(requests, "get", _get)
        return calls
    return _install


@pytest.mark.parametrize("repo", [
    "huggingface/transformers", " huggingface/transformers ", "huggingface/transformers.git",
    "https://github.com/huggingface/transformers", "github.com/huggingface/transformers/tree/main",
    "https://www.github.com/huggingface/transformers#readme",
])
def test_github_repo_parses_input_and_maps_repo_and_release(repo, github_http) -> None:
    calls = github_http({REPO_URL: FakeResponse(REPO_PAYLOAD),
                         REPO_URL + "/releases/latest": FakeResponse(RELEASE_PAYLOAD)})

    result = TOOL_FUNCTIONS["github_repo"](repo=repo)

    assert [c["url"] for c in calls] == [REPO_URL, REPO_URL + "/releases/latest"]
    assert all(c["headers"]["Accept"] == "application/vnd.github+json" and c["timeout"] == 30 for c in calls)
    assert "github_repo" in calls[0]["headers"]["User-Agent"]
    assert result == {"tool": "github_repo", "repo": "huggingface/transformers", "items": [{
        "title": "huggingface/transformers", "url": "https://github.com/huggingface/transformers",
        "source": "github.com", "summary": "Transformers library", "language": "Python",
        "license": "Apache-2.0", "updated": "2026-11-09T12:00:00Z", "archived": False,
        "metrics": {"stars": 150000, "forks": 30000, "open_issues": 1200},
        "latest_release": {"tag": "v5.0.0", "name": "v5.0.0", "published_at": "2026-11-01T00:00:00Z",
                           "url": "https://github.com/huggingface/transformers/releases/tag/v5.0.0"},
    }]}


def test_github_repo_without_release_returns_none_not_error(github_http) -> None:
    github_http({REPO_URL: FakeResponse(REPO_PAYLOAD), REPO_URL + "/releases/latest": FakeResponse(status_code=404)})

    result = TOOL_FUNCTIONS["github_repo"](repo="huggingface/transformers")

    assert "error" not in result and "release_error" not in result
    assert result["items"][0]["latest_release"] is None


def test_github_repo_release_failure_keeps_repo_info(github_http) -> None:
    github_http({REPO_URL: FakeResponse(REPO_PAYLOAD), REPO_URL + "/releases/latest": requests.Timeout("slow")})

    result = TOOL_FUNCTIONS["github_repo"](repo="huggingface/transformers")

    assert result["items"][0]["metrics"]["stars"] == 150000
    assert result["items"][0]["latest_release"] is None
    assert result["release_error"] == "Timeout: slow"


@pytest.mark.parametrize("repo", ["", "   ", None, 7, ["a/b"], "transformers", "a/b/c d",
                                  "https://gitlab.com/owner/repo", "-bad/repo", "owner/..", "owner/"])
def test_github_repo_bad_input_returns_error_without_network(repo, github_http) -> None:
    calls = github_http({})

    result = TOOL_FUNCTIONS["github_repo"](repo=repo)

    assert result["tool"] == "github_repo"
    assert result["error"] == "ValueError"
    assert result["message"]
    assert calls == []


@pytest.mark.parametrize("failure,expected", [
    (FakeResponse(status_code=404), ("HTTPError", "HTTP 404")),
    (FakeResponse(status_code=403), ("HTTPError", "HTTP 403")),
    (requests.Timeout("timed out"), ("Timeout", "timed out")),
    (requests.ConnectionError("offline"), ("ConnectionError", "offline")),
    (FakeResponse({"message": "no full_name"}), ("ValueError", "GitHub response must contain full_name")),
])
def test_github_repo_main_request_failure_returns_error_dict_and_skips_release(failure, expected, github_http) -> None:
    calls = github_http({REPO_URL: failure})

    result = TOOL_FUNCTIONS["github_repo"](repo="huggingface/transformers")

    assert [c["url"] for c in calls] == [REPO_URL]
    assert result == {"tool": "github_repo", "error": expected[0], "message": expected[1]}


# ---------------- Regression: social_search empty query (bug found by group eval G05) ----------------
# Run v5_B_group (G05): model called social_search(query="") instead of clarify. The starter tool sent the
# empty query to RapidAPI anyway (wasted request, 0 items, no error). Expected: error dict, no network call.

@pytest.mark.parametrize("query", ["", "   ", None])
def test_social_search_empty_query_returns_error_without_network(query, monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"timeline": []}))

    result = TOOL_FUNCTIONS["social_search"](query=query, search_type="Top")

    assert calls == []
    assert result["tool"] == "search_tweets"
    assert result["error"] == "ValueError"
    assert "query" in result["message"]


def test_social_search_valid_query_still_calls_api_with_stripped_query(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-key")
    calls = fake_http(FakeResponse({"timeline": [{"tweet_id": "1", "screen_name": "a", "text": "hi"}]}))

    result = TOOL_FUNCTIONS["social_search"](query="  Mistral ", search_type="Top")

    assert len(calls) == 1
    assert calls[0]["params"] == {"query": "Mistral", "search_type": "Top"}
    assert result["query"] == "Mistral"
    assert len(result["items"]) == 1

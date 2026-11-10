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

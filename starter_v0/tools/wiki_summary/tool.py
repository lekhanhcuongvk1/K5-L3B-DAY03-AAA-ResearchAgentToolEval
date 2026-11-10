from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err


SUPPORTED_LANGS = {"en", "vi"}
MAX_SUMMARY_CHARS = 1500
USER_AGENT = "Day03-Research-Agent/1.0 (wiki_summary; educational lab)"


def wiki_summary(query: str = "", lang: str = "en") -> dict[str, Any]:
    """Return the intro summary of the best-matching Wikipedia article; failures use the shared error dict."""
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty string (concept, person or organization name)")
        if not isinstance(lang, str) or lang.strip().lower() not in SUPPORTED_LANGS:
            raise ValueError(f"lang must be one of {sorted(SUPPORTED_LANGS)}")
        query = query.strip()
        lang = lang.strip().lower()

        # One call: search for the best title, then return its plain-text intro and URL.
        response = requests.get(
            f"https://{lang}.wikipedia.org/w/api.php",
            params={
                "action": "query",
                "format": "json",
                "formatversion": "2",
                "generator": "search",
                "gsrsearch": query,
                "gsrlimit": "1",
                "prop": "extracts|info",
                "exintro": "1",
                "explaintext": "1",
                "inprop": "url",
                "redirects": "1",
            },
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Wikipedia response must be a JSON object")
        if "query" not in payload:
            # MediaWiki omits `query` when the search has no hit: valid empty result, not an error.
            return {"tool": "wiki_summary", "query": query, "lang": lang, "items": []}
        pages = (payload.get("query") or {}).get("pages")
        if not isinstance(pages, list):
            raise ValueError("Wikipedia response query.pages must be a list")

        items = []
        for page in pages:
            if not isinstance(page, dict) or not isinstance(page.get("title"), str):
                raise ValueError("Wikipedia page must contain a title")
            extract = (page.get("extract") or "").strip()
            if len(extract) > MAX_SUMMARY_CHARS:
                extract = extract[: MAX_SUMMARY_CHARS - 3] + "..."
            items.append({
                "title": page["title"],
                "url": page.get("fullurl") or "",
                "source": f"{lang}.wikipedia.org",
                "summary": extract,
            })
        return {"tool": "wiki_summary", "query": query, "lang": lang, "items": items}
    except Exception as exc:
        return err("wiki_summary", exc)

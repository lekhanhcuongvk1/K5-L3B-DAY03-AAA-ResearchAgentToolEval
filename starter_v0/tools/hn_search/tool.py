from __future__ import annotations

from typing import Any

import requests

from tools._shared import TIMEOUT, err


ENDPOINTS = {
    "relevance": "https://hn.algolia.com/api/v1/search",
    "date": "https://hn.algolia.com/api/v1/search_by_date",
}
MAX_LIMIT = 20


def _parse_limit(limit: Any) -> int:
    # bool is a subclass of int; reject it explicitly. Accept int-like strings ("5") that models often send.
    if isinstance(limit, bool):
        raise ValueError("limit must be an integer between 1 and 20")
    if isinstance(limit, str) and limit.strip().isdigit():
        limit = int(limit.strip())
    if not isinstance(limit, int) or not 1 <= limit <= MAX_LIMIT:
        raise ValueError("limit must be an integer between 1 and 20")
    return limit


def hn_search(query: str = "", sort: str = "relevance", limit: int = 5) -> dict[str, Any]:
    """Search Hacker News stories via the Algolia HN API; failures use the shared error dict."""
    try:
        if not isinstance(query, str) or not query.strip():
            raise ValueError("query must be a non-empty keyword string")
        if not isinstance(sort, str) or sort.strip().lower() not in ENDPOINTS:
            raise ValueError(f"sort must be one of {sorted(ENDPOINTS)}")
        query = query.strip()
        sort = sort.strip().lower()
        limit = _parse_limit(limit)

        response = requests.get(
            ENDPOINTS[sort],
            params={"query": query, "tags": "story", "hitsPerPage": limit},
            headers={"Accept": "application/json"},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        hits = payload.get("hits") if isinstance(payload, dict) else None
        if not isinstance(hits, list):
            raise ValueError("HN response must contain a hits list")

        items = []
        for hit in hits:
            if not isinstance(hit, dict) or not hit.get("objectID") or not hit.get("title"):
                continue  # skip deleted/partial stories instead of failing the whole search
            discussion_url = f"https://news.ycombinator.com/item?id={hit['objectID']}"
            points = hit.get("points") or 0
            comments = hit.get("num_comments") or 0
            items.append({
                "title": hit["title"],
                "url": hit.get("url") or discussion_url,  # Ask/Show HN posts have no external url
                "discussion_url": discussion_url,
                "source": "news.ycombinator.com",
                "summary": f"{points} points, {comments} comments, by {hit.get('author') or 'unknown'}",
                "date": hit.get("created_at"),
                "metrics": {"points": points, "comments": comments},
            })
        return {"tool": "hn_search", "query": query, "sort": sort, "items": items[:limit]}
    except Exception as exc:
        return err("hn_search", exc)

from __future__ import annotations

import re
from typing import Any
from urllib.parse import quote, unquote

import requests

from tools._shared import TIMEOUT, err


CROSSREF_WORKS_URL = "https://api.crossref.org/works/"


def lookup_doi(doi: str = "") -> dict[str, Any]:
    """Retrieve one Crossref work by DOI; failures use the shared error contract."""
    try:
        if not isinstance(doi, str):
            raise ValueError("doi must be a non-empty DOI string")
        normalized = doi.strip()
        if re.match(r"^https?://(?:dx\.)?doi\.org/", normalized, re.IGNORECASE):
            normalized = unquote(re.sub(
                r"^https?://(?:dx\.)?doi\.org/", "", normalized, flags=re.IGNORECASE,
            ))
        elif normalized.lower().startswith("doi:"):
            normalized = normalized[4:].strip()
        if not re.fullmatch(r"10\.[0-9]{4,9}/\S+", normalized):
            raise ValueError("doi must look like 10.1234/example or https://doi.org/10.1234/example")

        # Encode the entire identifier: DOI suffixes can contain URL delimiters.
        response = requests.get(
            CROSSREF_WORKS_URL + quote(normalized, safe=""),
            headers={
                "Accept": "application/json",
                "User-Agent": "Day03-Research-Agent/1.0 (doi_lookup; educational lab)",
            },
            timeout=TIMEOUT,
        )
        response.raise_for_status()
        payload = response.json()
        work = payload.get("message") if isinstance(payload, dict) else None
        if not isinstance(work, dict):
            raise ValueError("Crossref response must contain a metadata object in message")
        if not isinstance(work.get("DOI"), str) or work["DOI"].lower() != normalized.lower():
            raise ValueError("Crossref response DOI is missing or does not match the request")

        titles = work.get("title") or []
        if not isinstance(titles, list) or any(not isinstance(title, str) for title in titles):
            raise ValueError("Crossref title must be a list of strings")
        authors = [
            " ".join(part for part in [author.get("given", ""), author.get("family", "")] if part)
            or author.get("name", "")
            for author in (work.get("author") or [])
        ]
        date_parts = (work.get("published") or {}).get("date-parts") or []
        item = {
            "doi": work["DOI"],
            "title": titles[0] if titles else "",
            "authors": [author for author in authors if author],
            "publisher": work.get("publisher") or "",
            "year": date_parts[0][0] if date_parts and date_parts[0] else None,
            "url": "https://doi.org/" + quote(work["DOI"], safe="/"),
            "source": "crossref.org",
        }
        return {"tool": "doi_lookup", "doi": normalized, "items": [item]}
    except Exception as exc:
        return err("doi_lookup", exc)

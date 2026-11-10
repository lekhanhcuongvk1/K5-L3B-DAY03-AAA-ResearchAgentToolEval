from __future__ import annotations

import re
from typing import Any

import requests

from tools._shared import TIMEOUT, err


API = "https://api.github.com/repos"
HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "Day03-Research-Agent/1.0 (github_repo; educational lab)",
}
# owner: 1-39 chars, letters/digits/hyphen; repo: letters/digits/._-
_SLUG = re.compile(r"^([A-Za-z0-9](?:[A-Za-z0-9-]{0,38}))/([A-Za-z0-9._-]+)$")
_URL = re.compile(r"^(?:https?://)?(?:www\.)?github\.com/([^/\s]+)/([^/\s#?]+)", re.IGNORECASE)


def _parse_repo(repo: Any) -> tuple[str, str]:
    if not isinstance(repo, str) or not repo.strip():
        raise ValueError("repo must be 'owner/repo' or a github.com repository URL")
    text = repo.strip()
    match = _URL.match(text)
    if match:
        text = f"{match.group(1)}/{match.group(2)}"
    if text.endswith(".git"):
        text = text[:-4]
    slug = _SLUG.match(text.rstrip("/"))
    if not slug or slug.group(2) in {".", ".."}:
        raise ValueError("repo must be 'owner/repo' or a github.com repository URL")
    return slug.group(1), slug.group(2)


def _latest_release(owner: str, name: str) -> tuple[dict[str, Any] | None, str | None]:
    """Latest release is optional: 404 means 'no release', other failures are reported but not fatal."""
    try:
        response = requests.get(f"{API}/{owner}/{name}/releases/latest", headers=HEADERS, timeout=TIMEOUT)
        if response.status_code == 404:
            return None, None
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("release response must be a JSON object")
        return {
            "tag": data.get("tag_name") or "",
            "name": data.get("name") or "",
            "published_at": data.get("published_at"),
            "url": data.get("html_url") or "",
        }, None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def github_repo(repo: str = "") -> dict[str, Any]:
    """Return metadata (+ latest release) for one public GitHub repository; failures use the shared error dict."""
    try:
        owner, name = _parse_repo(repo)
        response = requests.get(f"{API}/{owner}/{name}", headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict) or not isinstance(data.get("full_name"), str):
            raise ValueError("GitHub response must contain full_name")

        release, release_error = _latest_release(owner, name)
        item = {
            "title": data["full_name"],
            "url": data.get("html_url") or f"https://github.com/{data['full_name']}",
            "source": "github.com",
            "summary": data.get("description") or "",
            "language": data.get("language") or "",
            "license": (data.get("license") or {}).get("spdx_id") or "",
            "updated": data.get("pushed_at"),
            "archived": bool(data.get("archived")),
            "metrics": {
                "stars": data.get("stargazers_count") or 0,
                "forks": data.get("forks_count") or 0,
                "open_issues": data.get("open_issues_count") or 0,
            },
            "latest_release": release,
        }
        result: dict[str, Any] = {"tool": "github_repo", "repo": f"{owner}/{name}", "items": [item]}
        if release_error:
            result["release_error"] = release_error
        return result
    except Exception as exc:
        return err("github_repo", exc)

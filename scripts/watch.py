#!/usr/bin/env python3
"""Poll vendor security advisory sources and notify new items.

Pipeline generico: no editar. Tus datos van en config.py (ver config.example.py).
State (ids ya notificados) se persiste en state/seen.json.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path

import feedparser

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import config
from notifiers import get_notifier

STATE_PATH = Path(__file__).resolve().parent.parent / "state" / "seen.json"
GITHUB_TOKEN = os.environ.get("GH_API_TOKEN")

GITHUB_API_HEADERS = {"Accept": "application/vnd.github+json"}
if GITHUB_TOKEN:
    GITHUB_API_HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"

notify = get_notifier(config.NOTIFIER)


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return {}


def save_state(state):
    STATE_PATH.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def fetch_feed_items(url):
    req = urllib.request.Request(url, headers={"User-Agent": "vendor-security-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        raw = resp.read()
    parsed = feedparser.parse(raw)
    return [
        {"id": e.get("id") or e.get("link"), "title": e.get("title", "(sin titulo)"), "link": e.get("link", "")}
        for e in parsed.entries
    ]


def fetch_github_advisories(repo):
    url = f"https://api.github.com/repos/{repo}/security-advisories"
    req = urllib.request.Request(url, headers={**GITHUB_API_HEADERS, "User-Agent": "vendor-security-watch/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return [
        {
            "id": a["ghsa_id"],
            "title": f"[{(a.get('severity') or 'unknown').upper()}] {a.get('summary', '(sin resumen)')}",
            "link": a.get("html_url", ""),
        }
        for a in data
    ]


def matches_keywords(item, keywords):
    if not keywords:
        return True
    return any(kw in item["title"].lower() for kw in keywords)


def main():
    state = load_state()
    changed = False

    for source in config.SOURCES:
        name = source["name"]
        try:
            if source["type"] in ("rss", "atom"):
                items = fetch_feed_items(source["url"])
            elif source["type"] == "github_advisories":
                items = fetch_github_advisories(source["repo"])
            else:
                continue
        except Exception as exc:  # network/parse errors shouldn't kill other sources
            print(f"[error] fallo al obtener {name}: {exc}", file=sys.stderr)
            continue

        seen_ids = set(state.get(name, []))
        is_first_run = name not in state
        new_items = [i for i in items if i["id"] not in seen_ids]
        keywords = source.get("keywords")

        if not is_first_run:
            for item in new_items:
                if matches_keywords(item, keywords):
                    notify(name, item)
        elif new_items:
            print(f"[info] primer run para {name}: se guardan {len(new_items)} items sin notificar")

        if new_items:
            changed = True
            state[name] = list(seen_ids | {i["id"] for i in items})[-200:]

    if changed:
        save_state(state)


if __name__ == "__main__":
    main()

"""Simple RSS fetcher using feedparser.

Reads feed URLs from ``rss_config.json`` or the ``RSS_FEEDS`` environment
variable and returns newly discovered articles.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Dict, List

import feedparser

CONFIG_ENV_VAR = "RSS_CONFIG"
FEEDS_ENV_VAR = "RSS_FEEDS"
SEEN_FILE = Path("seen_articles.json")


def get_feed_urls(config_path: str | None = None) -> List[str]:
    """Return feed URLs from a config file or environment variable.

    Priority is given to the ``RSS_FEEDS`` environment variable where multiple
    URLs can be comma separated. Otherwise, a JSON configuration file is
    loaded. The file path can be supplied via ``config_path`` or the
    ``RSS_CONFIG`` environment variable. If none of these are provided, the
    default ``rss_config.json`` is used.
    """
    env_feeds = os.getenv(FEEDS_ENV_VAR)
    if env_feeds:
        return [u.strip() for u in env_feeds.split(",") if u.strip()]

    path = config_path or os.getenv(CONFIG_ENV_VAR) or "rss_config.json"
    config_file = Path(path)
    if config_file.exists():
        with config_file.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
        if isinstance(data, list):
            return data
        return data.get("feeds", [])
    return []


def load_seen() -> set[str]:
    if SEEN_FILE.exists():
        with SEEN_FILE.open("r", encoding="utf-8") as handle:
            return set(json.load(handle))
    return set()


def save_seen(seen: set[str]) -> None:
    with SEEN_FILE.open("w", encoding="utf-8") as handle:
        json.dump(sorted(seen), handle, indent=2)


def fetch_new_articles(config_path: str | None = None) -> List[Dict[str, str]]:
    """Fetch new articles from configured RSS feeds.

    Returns a list of dictionaries each containing ``title`` and ``link`` keys.
    Only articles whose links have not been seen before are returned.
    """
    urls = get_feed_urls(config_path)
    seen = load_seen()
    new_articles: List[Dict[str, str]] = []

    for url in urls:
        feed = feedparser.parse(url)
        for entry in getattr(feed, "entries", []):
            link = entry.get("link")
            title = entry.get("title", "")
            if link and link not in seen:
                new_articles.append({"title": title, "link": link})
                seen.add(link)

    if new_articles:
        save_seen(seen)
    return new_articles


if __name__ == "__main__":
    articles = fetch_new_articles()
    for article in articles:
        print(f"{article['title']} - {article['link']}")

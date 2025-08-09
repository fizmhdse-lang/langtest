import json
from types import SimpleNamespace
from pathlib import Path
import sys

import pytest

sys.path.append(str(Path(__file__).resolve().parent.parent))
import rss_fetcher


def test_get_feed_urls_from_config(tmp_path):
    config = tmp_path / "config.json"
    feeds = ["http://example.com/feed"]
    config.write_text(json.dumps(feeds))
    result = rss_fetcher.get_feed_urls(str(config))
    assert result == feeds


def test_get_feed_urls_env_overrides_config(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    feeds = ["http://example.com/feed"]
    config.write_text(json.dumps(feeds))
    env_feeds = "http://env1.com, http://env2.com"
    monkeypatch.setenv(rss_fetcher.FEEDS_ENV_VAR, env_feeds)
    result = rss_fetcher.get_feed_urls(str(config))
    assert result == ["http://env1.com", "http://env2.com"]


def test_fetch_new_articles(tmp_path, monkeypatch):
    config = tmp_path / "config.json"
    feeds = ["http://example.com/feed"]
    config.write_text(json.dumps(feeds))

    dummy_feed = SimpleNamespace(entries=[{"link": "http://article1", "title": "Article 1"}])
    monkeypatch.setattr(rss_fetcher, "feedparser", SimpleNamespace(parse=lambda url: dummy_feed))
    monkeypatch.setattr(rss_fetcher, "SEEN_FILE", tmp_path / "seen.json")

    articles = rss_fetcher.fetch_new_articles(str(config))
    assert articles == [{"title": "Article 1", "link": "http://article1"}]

    # second run should yield no new articles because link is now seen
    articles_again = rss_fetcher.fetch_new_articles(str(config))
    assert articles_again == []

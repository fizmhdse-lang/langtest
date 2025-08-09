from __future__ import annotations

"""LangChain loader wrapping the ``rss_fetcher`` utility.

This loader converts newly discovered RSS articles into LangChain
``Document`` objects so they can be consumed by downstream chains.
"""
from langchain_community.document_loaders.base import BaseLoader
from langchain_core.documents import Document

from rss_fetcher import fetch_new_articles


class RSSFetcherLoader(BaseLoader):
    """Load documents from configured RSS feeds.

    Parameters
    ----------
    config_path:
        Optional path to a JSON configuration file listing feed URLs.
        Falls back to environment variables as described in
        :func:`rss_fetcher.get_feed_urls`.
    """

    def __init__(self, config_path: str | None = None):
        self.config_path = config_path

    def load(self) -> list[Document]:
        """Return newly fetched articles as ``Document`` instances."""
        articles = fetch_new_articles(self.config_path)
        return [
            Document(page_content=article["title"], metadata={"source": article["link"]})
            for article in articles
        ]

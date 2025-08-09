from types import SimpleNamespace
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))

from langchain_core.documents import Document

from rss_langchain_loader import RSSFetcherLoader


def test_loader_returns_documents(monkeypatch):
    articles = [{"title": "Article 1", "link": "http://article1"}]
    monkeypatch.setattr("rss_langchain_loader.fetch_new_articles", lambda config: articles)

    loader = RSSFetcherLoader()
    docs = loader.load()
    assert docs == [Document(page_content="Article 1", metadata={"source": "http://article1"})]

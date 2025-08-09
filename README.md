# langtest

test

## RSS Fetcher

`rss_fetcher.py` fetches new articles from RSS feeds using the `feedparser`
package. Feed URLs are read from `rss_config.json` or the `RSS_FEEDS`
environment variable. Run the module directly to print newly discovered
article titles and links.

## LangChain Loader

`rss_langchain_loader.py` exposes `RSSFetcherLoader` which wraps the RSS
fetcher and returns feed entries as LangChain `Document` objects.

```python
from rss_langchain_loader import RSSFetcherLoader

loader = RSSFetcherLoader("rss_config.json")
for doc in loader.load():
    print(doc.metadata["source"], doc.page_content)
```

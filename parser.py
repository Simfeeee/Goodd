import feedparser

RSS_FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    "https://www.aljazeera.com/xml/rss/all.xml"
]

def get_latest_news():
    news_items = []
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)
        if feed.entries:
            entry = feed.entries[0]
            news_items.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })
    return news_items
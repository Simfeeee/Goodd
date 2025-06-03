
import feedparser

def fetch_realnoevremya():
    url = "https://realnoevremya.ru/feed"
    feed = feedparser.parse(url)
    articles = []
    for entry in feed.entries:
        articles.append({
            "id": entry.id,
            "title": entry.title,
            "link": entry.link,
            "summary": entry.summary,
            "source": "Реальное время"
        })
    return articles

import feedparser
import json
from bs4 import BeautifulSoup
from pathlib import Path

def get_json_cfg()->dict:
    cfg = None  # a dict
    with open(Path(r"..\rss_cfg.json").resolve(), 'r') as fp:
        cfg = json.load(fp)
    return cfg

def get_headlines_articles(_rss_cfg:dict)->tuple[str,str]:
    headlines = []
    articles = []
    for section, news_entities in _rss_cfg.items():
        for source, feed_link in news_entities.items():
            feed = feedparser.parse(feed_link)
            for entry in feed.entries[:5]:
                headlines.append(entry.title_detail.value)
                print(entry.title_detail.value)
#end def

if __name__=='__main__':
    rss_cfg = get_json_cfg()
    (headlines, articles) = get_headlines_articles(rss_cfg)
    print('Starting Newspaper aggregator...')
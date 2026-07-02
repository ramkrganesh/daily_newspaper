import feedparser
import json
import logging
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

logging_lvl = logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(filename='news_logger.log', filemode='w', level=logging_lvl,
                    encoding='utf-8')

# CONFIGURATIONS ----------------------------------------------------
NUM_HEADLINES = 5
NUM_ARTICLES = 2
# -------------------------------------------------------------------

def get_json_cfg()->dict:
    cfg = None  # a dict
    with open(Path(r"../rss_cfg.json").resolve(), 'r') as fp:
        cfg = json.load(fp)
    return cfg

def get_headlines_articles(_rss_cfg:dict)->tuple[dict,dict]:
    def _content_cleanup(text, _soup=False):
        if _soup:
            text = BeautifulSoup(text, 'html.parser').getText()
        #end if
        clean_text = (text
                      .replace("\u00A0", ' ')
                      .replace('&amp;', ' '))  # cleanup NBSP, &amp;
        return clean_text
    #end def

    def _append_headline(srcs, headln)->None:
        if srcs in headlines_dict:
            headlines_dict[srcs].append(headln)
        else:
            headlines_dict.update({srcs: [headln]})
    #end def

    headlines_dict = {}
    articles = {}
    for news_type, sources in _rss_cfg.items():
        for source, rss_link in sources.items():
            logger.debug(f"----- Fetching {source} -----")
            feeds = feedparser.parse(rss_link)
            for entry in feeds.entries[:NUM_HEADLINES]:
                headline = _content_cleanup(entry.title_detail.value)
                summary = _content_cleanup(entry.summary, _soup=True)
                news_item = headline + '\n' + summary.strip()
                _append_headline(source, news_item)
                logger.debug(f"{news_item}")
            #end for
            time.sleep(1)
        #end for
    #end for
    return headlines_dict,articles
#end def

if __name__=='__main__':
    rss_cfg = get_json_cfg()
    (headlines_lst, articles_lst) = get_headlines_articles(rss_cfg)

import feedparser
import json
from bs4 import BeautifulSoup
from pathlib import Path

def get_json_cfg()->dict:
    cfg = None  # a dict
    with open(Path(r"..\rss_cfg.json").resolve(), 'r') as fp:
        cfg = json.load(fp)
    return cfg

if __name__=='__main__':
    rss_cfg = get_json_cfg()
    print('Starting Newspaper aggregator...')
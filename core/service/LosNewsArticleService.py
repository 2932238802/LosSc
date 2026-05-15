import requests
from bs4 import BeautifulSoup
from typing import Dict,Any,List
from core.crawler.LosNewsArticleCrawler import LosNewsArticleCrawler

class LosNewsArticleService:
    def Lf_get_article(self,url:str) -> Dict[str,Any]:
        crawler = LosNewsArticleCrawler(url=url)
        return crawler.Lf_run()

from typing import Any, List, Dict
from core.crawler.LosBaseCrawler import LosBaseCrawler
from bs4 import BeautifulSoup
import requests

class LosNewsCrawler(LosBaseCrawler):
    
    
    """
    init 
    
    初始化    
    """
    def __init__(
        self, 
        url: str, 
        source:str,
        timeout: int = 10,
        ) -> None:
        super().__init__(url, timeout)
        self.L_source = source
    
    
        
    """
    private tool
    
    获取数据
    """
    def _Lf_fetch(self) -> bytes:
        res= requests.get(self.L_url,timeout=self.L_timeout)
        if res.status_code != 200:
            raise RuntimeError(f"请求失败，状态码：{res.status_code}")
        return res.content
    
    
    
    """
    private tool
    
    解析
    """
    def _Lf_parse(self, data: Any) -> List[Dict[str,Any]]:
        bf = BeautifulSoup(data,"xml")
        items = bf.find_all("item")
        news_list: List[Dict[str, Any]] = []
        for item in items:
            title_tag = item.find("title")
            link_tag = item.find("link")
            summary_tag = item.find("description")
            published_tag = item.find("pubDate")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = link_tag.get_text(strip=True) if link_tag else ""
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            published = published_tag.get_text(strip=True) if published_tag else ""
            if title and link:
                news_list.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                    "source": self.L_source
                })
        return news_list
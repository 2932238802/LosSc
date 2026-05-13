
from typing import Any, List, Dict
from core.crawler.LosBaseCrawler import LosBaseCrawler
from bs4 import BeautifulSoup
import requests


# 注意 RSS 的 格式
# <rss>
#   <channel>
#     <item>
#       <title>新闻标题</title>
#       <link>新闻链接</link>
#       <description>新闻摘要</description>
#       <pubDate>发布时间</pubDate>
#       <media:thumbnail url="https://example.com/a.jpg" />
#     </item>
#     <item>
#       ...
#     </item>
#   </channel>
# </rss>



class LosNewsCrawler(LosBaseCrawler):
    
    """
    init 
    
    初始化    
    """
    def __init__(
        self, 
        url: str, 
        news_name: str,
        column_name: str,
        timeout: int = 10,
        ) -> None:
        super().__init__(url, timeout)
        self.L_news_name = news_name
        self.L_column_name = column_name
    
    
        
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
        # [
        #     {
                
        #     },
        #     {
                
        #     }
        # ] # type: ignore
        for item in items:
            title_tag = item.find("title")
            link_tag = item.find("link")
            summary_tag = item.find("description")
            published_tag = item.find("pubDate")
            media_thumbnail = item.find("media:thumbnail")
            media_content = item.find("media:content")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = link_tag.get_text(strip=True) if link_tag else ""
            summary = summary_tag.get_text(strip=True) if summary_tag else ""
            published = published_tag.get_text(strip=True) if published_tag else ""
            image_url = media_thumbnail.get("url","") if media_thumbnail is not None else (media_content.get("url", "") if media_content is not None else "")
            if title and link:
                news_list.append({
                    "title": title,
                    "link": link,
                    "summary": summary,
                    "published": published,
                    "news_name": self.L_news_name,
                    "column_name": self.L_column_name,
                    "image_url" : image_url
                })
        return news_list

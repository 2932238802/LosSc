
from typing import Any,Dict,List
import requests
from core.crawler.LosBaseCrawler import LosBaseCrawler
from bs4 import BeautifulSoup
from urllib.parse import urljoin

"""
新闻文章
"""
class LosNewsArticleCrawler(LosBaseCrawler):
    
    def __init__(self, url: str, timeout: int = 10) -> None:
        super().__init__(url,timeout)
    
    
    """
    获取 文章信息    
    """
    def _Lf_fetch(self) -> Any:
        res = requests.get(
            url= self.L_url,
            timeout= self.L_timeout,
            headers={
                "User-Agent":"Mozilla/5.0"
            }
        )
        
        if res.status_code != 200:
            raise RuntimeError(f"请求失败 状态码{res.status_code}")
        res.encoding = res.apparent_encoding
        return res.text
        
        
        
    """
    解析文章内容    
    """
    def _Lf_parse(self, data: Any) -> Any:
        soup = BeautifulSoup(data,"lxml")
        title = ""
        
        if soup.title is not None:
            title = soup.title.get_text(strip=True)
            
        paragraph:List[str] = []

        for p in soup.find_all('p'):
            text = p.get_text(strip=True)
            paragraph.append(text)
            
        image:List[str] = []
        for img in soup.find_all("img"):
            src  = img.get("src","")
            if not isinstance(src, str) or not src:
                continue
            image.append(urljoin(self.L_url, src))
            
        content = "\n\n".join(paragraph)
        return {
            "url": self.L_url,
            "title": title,
            "content": content,
            "images": image[:10],
            "content_length": len(content),
            "image_count": len(image),
        }
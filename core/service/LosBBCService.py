from typing import List,Dict,Any
from core.crawler.LosNewsCrawler import LosNewsCrawler
from core.LosConfig import BBC_NEWS_TIME_OUT,BBC_NEWS_URL
from db.LosDb import LosDb

class LosBBCService:
    
    def __init__(self) -> None:
        self.L_crawler = LosNewsCrawler(
            BBC_NEWS_URL,
            "BBC",
            BBC_NEWS_TIME_OUT
        )
        

    
    """
    private tool
    获取数据    
    """
    def _Lf_get_data(self) -> List[Dict[str, Any]]:
        return self.L_crawler.Lf_run()
    
    

    
    """
    public tool
    
    保存到数据库    
    返回一个结果数组
    """
    def Lf_save_to_db(self) -> Dict[str, int]:
        news_list = self._Lf_get_data()
        insert_number = 0
        ignore_number = 0
             
        #  一次调用 
        # __exit__ 
        # __enter__
        with LosDb() as db:
            for news in news_list:
                is_insert:bool = db.Lf_insert_news_db(
                    title=news["title"],
                    link=news["link"],
                    summary=news["summary"],
                    published=news["published"],
                    source=news.get("source",""),
                    image_url=news.get("image_url", "")
                )
                if is_insert:
                    insert_number+=1
                else:
                    ignore_number+=1
            total_number = db.Lf_get_count()
             
            
        return dict({
            "crawl_number": len(news_list),
            "insert_number": insert_number,
            "ignore_number": ignore_number,
            "total_number" : total_number
        })
        
        
        
        
    """
    public tool
    
    """
    def Lf_get_latest_news(self,limit:int=20) -> List[Dict[str,Any]]:
        with LosDb() as db:
            return db.Lf_get_latest_news(limit)
        
        
    
    """
    public tool get
    """
    def Lf_get_latest_news_by_page(
        self,
        page:int = 1,
        page_size: int = 20
        ) -> Dict[str, Any]:
        
        with LosDb() as db:
            # id,title,link,summary,published,source,image_url,created_a
            items = db.Lf_get_latest_news_by_page(page=page,page_size=page_size)
            total_number = db.Lf_get_count()
        
        total_page = (total_number + page_size - 1) // page_size
        return{
            "page":page,
            "page_size" : page_size,
            "total_number": total_number,
            "total_page" : total_page,
            "has_next" : page < total_page,
            "has_prev" : page > 1,
            "items":items
        }
        
            
        
    
    
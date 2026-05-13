from typing import List, Dict, Any
from core.crawler.LosNewsCrawler import LosNewsCrawler
from core.LosConfig import (
    RMW_NEWS_NAME,
    RMW_NEWS_TIME_OUT,
    RMW_NEWS_CHANNELS,
)
from db.LosDb import LosDb

class LosRMWService:
    """
    人民网新闻服务
    RMW = RenMinWang
    支持多栏目抓取
    """

    """
    private tool
    
    抓取单个栏目的数据
    """
    def _Lf_fetch_single_column_data(
        self,
        column_name: str,
        url: str
    ) -> List[Dict[str, Any]]:
        crawler = LosNewsCrawler(
            url=url,
            news_name=RMW_NEWS_NAME,
            column_name=column_name,
            timeout=RMW_NEWS_TIME_OUT
        )
        return crawler.Lf_run()



    """
    public tool
    
    保存到数据库
    {
    "crawl_number": 150,
    "insert_number": 120,
    "ignore_number": 30,
    "total_number": 120,
    "channels": [
        {"column_name": "top",      "success": true, "crawl_number": 30, "insert_number": 25, "ignore_number": 5},
        {"column_name": "world",    "success": true, "crawl_number": 30, "insert_number": 30, "ignore_number": 0},
        {"column_name": "business", "success": false, "error": "请求失败，状态码：404", "crawl_number": 0, "insert_number": 0, "ignore_number": 0},
        ...
    ]
    }
    """
    def Lf_save_to_db(self) -> Dict[str, Any]:
        channel_results: List[Dict[str, Any]] = []
        total_crawl = 0
        total_insert = 0
        total_ignore = 0
        with LosDb() as db:
            for channel in RMW_NEWS_CHANNELS:
                column_name = channel["column_name"]
                url = channel["url"]
                insert_number = 0
                ignore_number = 0
                crawl_number = 0

                try:
                    news_list = self._Lf_fetch_single_column_data(column_name, url)
                except Exception as e:
                    channel_results.append({
                        "column_name": column_name,
                        "success": False,
                        "error": str(e),
                        "crawl_number": 0,
                        "insert_number": 0,
                        "ignore_number": 0,
                    })
                    continue

                crawl_number = len(news_list)

                for news in news_list:
                    is_insert: bool = db.Lf_insert_news_db(
                        title=news["title"],
                        link=news["link"],
                        summary=news["summary"],
                        published=news["published"],
                        news_name=news.get("news_name", ""),
                        column_name=news.get("column_name", ""),
                        image_url=news.get("image_url", "")
                    )
                    if is_insert:
                        insert_number += 1
                    else:
                        ignore_number += 1

                total_crawl += crawl_number
                total_insert += insert_number
                total_ignore += ignore_number

                channel_results.append({
                    "column_name": column_name,
                    "success": True,
                    "crawl_number": crawl_number,
                    "insert_number": insert_number,
                    "ignore_number": ignore_number,
                })

            total_number = db.Lf_get_count() # 返回所有的新闻结果

        return {
            "crawl_number": total_crawl,
            "insert_number": total_insert,
            "ignore_number": total_ignore,
            "total_number": total_number,
            "channels": channel_results,
        }
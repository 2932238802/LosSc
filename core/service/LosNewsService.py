from typing import List, Dict, Any

from db.LosDb import LosDb


class LosNewsService:

    """
    public tool

    获取最新新闻（不分来源）
    """
    def Lf_get_latest_news(
        self,
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        with LosDb() as db:
            return db.Lf_get_latest_news(limit)


    """
    public tool

    分页获取所有新闻（混合流，按 id DESC）
    """
    def Lf_get_latest_news_by_page(
        self,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:

        with LosDb() as db:
            items = db.Lf_get_latest_news_by_page(
                page=page,
                page_size=page_size
            )
            total_number = db.Lf_get_count()

        total_page = (total_number + page_size - 1) // page_size

        return {
            "page": page,
            "page_size": page_size,
            "total_number": total_number,
            "total_page": total_page,
            "has_next": page < total_page,
            "has_prev": page > 1,
            "items": items
        }


    """
    public tool

    按 news_name 
    分页获取新闻（某个新闻网站下的全部新闻）
    """
    def Lf_get_news_by_news_name_and_page(
        self,
        news_name: str,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:

        with LosDb() as db:
            items = db.Lf_get_latest_news_by_news_name_and_page(
                news_name=news_name,
                page=page,
                page_size=page_size
            )
            total_number = db.Lf_get_count_by_news_name(news_name)

        total_page = (total_number + page_size - 1) // page_size

        return {
            "news_name": news_name,
            "page": page,
            "page_size": page_size,
            "total_number": total_number,
            "total_page": total_page,
            "has_next": page < total_page,
            "has_prev": page > 1,
            "items": items
        }


    """
    public tool

    按 news_name + column_name 分页获取新闻 某个网站下某个栏目
    """
    def Lf_get_news_by_news_name_and_column_name_and_page(
        self,
        news_name: str,
        column_name: str,
        page: int = 1,
        page_size: int = 20
    ) -> Dict[str, Any]:

        with LosDb() as db:
            items = db.Lf_get_latest_news_by_news_name_and_column_name_and_page(
                news_name=news_name,
                column_name=column_name,
                page=page,
                page_size=page_size
            )
            total_number = db.Lf_get_count_by_news_name_and_column_name(
                news_name=news_name,
                column_name=column_name
            )

        total_page = (total_number + page_size - 1) // page_size

        return {
            "news_name": news_name,
            "column_name": column_name,
            "page": page,
            "page_size": page_size,
            "total_number": total_number,
            "total_page": total_page,
            "has_next": page < total_page,
            "has_prev": page > 1,
            "items": items
        }


    """
    public tool get
    
    获取新闻网站列表
    """
    def Lf_get_news_names(self) -> List[str]:
        with LosDb() as db:
            return db.Lf_get_news_names()


    """
    public tool get
    
    获取指定新闻网站下的栏目列表
    """
    def Lf_get_column_names_by_news_name(self, news_name: str) -> List[str]:
        with LosDb() as db:
            return db.Lf_get_column_names_by_news_name(news_name)

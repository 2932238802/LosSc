
from fastapi import APIRouter,Query
from typing import Dict,Any
from core.service.LosNewsService import LosNewsService
from core.service.LosNewsArticleService import LosNewsArticleService
from core.response.LosNewsResponse import LF_LosNewsSuccess

"""
新闻路由

tags 就是一个分组的作用
"""
LosNewsRouter = APIRouter(
    prefix="/api/news",
    tags=["news"]
)



"""
获取最新新闻（混合流，不分来源）
"""
@LosNewsRouter.get("/latest")
def LF_get_latest_news(limit: int = Query(10, ge=1, le=100)):
    service = LosNewsService()
    news= service.Lf_get_latest_news(limit)
    return LF_LosNewsSuccess(
        data = {
            "count": len(news),
            "items": news
        },
        message= "latest news fetched"
    )



"""
分页获取新闻（混合流，按时间）
用于手机端 快捷信息 页面
"""
@LosNewsRouter.get("/bypage")
def LF_get_latest_news_by_page(
    page: int = Query(1,ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    service = LosNewsService()
    res = service.Lf_get_latest_news_by_page(
        page=page,
        page_size=page_size
    )
    return LF_LosNewsSuccess(
        message="news page fetched",
        data= res
    )



"""
获取全部新闻网站列表
用于手机端 或者 电脑端
展示有哪些新闻网站
"""
@LosNewsRouter.get("/news_names")
def LF_get_news_names():
    service = LosNewsService()
    res = service.Lf_get_news_names()
    return LF_LosNewsSuccess(
        message="news names fetched",
        data={
            "count" : len(res),
            "items": res
        }
    )



"""
获取指定新闻网站下的栏目列表
/api/news/columns?news_name=BBC
"""
@LosNewsRouter.get("/columns")
def LF_get_column_names_by_news_name(
    news_name: str = Query(...)
):
    service = LosNewsService()
    res = service.Lf_get_column_names_by_news_name(news_name)
    return LF_LosNewsSuccess(
        message="column names fetched",
        data={
            "news_name": news_name,
            "count" : len(res),
            "items": res
        }
    )



"""
按新闻网站分页获取新闻
例如 /api/news/by_news_name/bypage?news_name=BBC
"""
@LosNewsRouter.get("/by_news_name/bypage")
def LF_get_news_by_news_name_and_page(
    news_name: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50)
):
    service = LosNewsService()
    res = service.Lf_get_news_by_news_name_and_page(
        news_name=news_name,
        page=page,
        page_size=page_size
    )
    return LF_LosNewsSuccess(
        message="news_name page fetched",
        data=res
    )



"""
按 新闻网站 + 栏目 分页获取新闻
/api/news/by_news_name_and_column/bypage?news_name=BBC&column_name=top
"""
@LosNewsRouter.get("/by_news_name_and_column/bypage")
def LF_get_news_by_news_name_and_column_name_and_page(
    news_name: str = Query(...),
    column_name: str = Query(...),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=50)
):
    service = LosNewsService()
    res = service.Lf_get_news_by_news_name_and_column_name_and_page(
        news_name=news_name,
        column_name=column_name,
        page=page,
        page_size=page_size
    )
    return LF_LosNewsSuccess(
        message="news_name and column_name page fetched",
        data=res
    )



"""
获取文本信息
"""
@LosNewsRouter.get("/article/preview")
def LF_preview_article(url:str = Query(...)) -> Dict[str,Any]:
    service = LosNewsArticleService()
    res = service.Lf_get_article(url)
    return LF_LosNewsSuccess(
        message="article fetched",
        data = res
    )


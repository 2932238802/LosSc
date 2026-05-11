from fastapi import FastAPI,Query
from core.service.LosBBCService import LosBBCService
from typing import Dict,Any
app = FastAPI(
    title="LosSc",
    version="0.01",
    description="los scraw api"
)

    

"""
根节点
"""
@app.get("/")
def root():
    return {
        "message": "Hello World"
    }
    
    

"""
获取 BBC 最新新闻
"""
@app.get("/api/news/bbc/latest")
def LF_get_latest_news_bbc(limit: int = Query(10, ge=1, le=100)):
    service = LosBBCService()
    news= service.Lf_get_latest_news(limit)
    return {
        "success": True,
        "message": "latest news fetched",
        "data": {
            "count": len(news),
            "items": news
        }
    }



"""
获取 BBC 最新的几个新闻
"""
@app.get("/api/news/bbc/bypage")
def LF_get_latest_news_by_page_bbc(
    page: int = Query(1,ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    service = LosBBCService()
    # 返回的结果是这个
    # Dict[str, Any]
    res = service.Lf_get_latest_news_by_page(
        page=page,
        page_size=page_size
    )
    return {
        "success": True,
        "message": "news page fetched",
        "data": res
    }




"""
抓取 BBC 数据
"""
@app.post("/api/crawler/bbc")
def LF_get_craw_bbc() -> Dict[str, Any]:
    service = LosBBCService()
    res = service.Lf_save_to_db()
    return {
        "success": True,
        "message": "BBC news crawl finished",
        "data": res
    }

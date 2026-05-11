from fastapi import FastAPI
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
获取 最新新闻
"""
@app.get("/api/news/latest")
def LF_get_latest_news(limit:int = 10):
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


from typing import Dict,Any
from core.service.LosBBCService import LosBBCService
from core.service.LosRMWService import LosRMWService
from core.response.LosNewsResponse import LF_LosNewsSuccess
from fastapi import APIRouter

LosCrawlerRouter = APIRouter(
    prefix="/api/crawler",
    tags=["crawler"]
)



"""
抓取 BBC 数据
"""
@LosCrawlerRouter.post("/bbc")
def LF_get_craw_bbc() -> Dict[str, Any]:
    service = LosBBCService()
    res = service.Lf_save_to_db()
    return LF_LosNewsSuccess(
        message="BBC news crawl finished",
        data=res
    )



"""
抓取 人民网 要闻快讯
"""
@LosCrawlerRouter.post("/rmw")
def LF_get_craw_rmw() -> Dict[str, Any]:
    service = LosRMWService()
    res = service.Lf_save_to_db()
    return LF_LosNewsSuccess(
        message="RMW news crawl finished",
        data=res
    )

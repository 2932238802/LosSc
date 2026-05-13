
from typing import Dict,List,Any


"""
爬虫新闻时候的正确结果
"""
def LF_LosNewsSuccess(
    data:Any = None,
    message : str = "news ope success"
):
    return {
        "success" : True,
        "message" : message,
        "data" : data
    }    
    


"""
爬虫新闻时候的错误结果
"""
def LF_LosNewsFail(
    message: str = "news ope failed",
    data: Any = None
) -> Dict[str, Any]:
    return {
        "success": False,
        "message": message,
        "data": data
    }
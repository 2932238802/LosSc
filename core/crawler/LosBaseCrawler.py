from abc import ABC,abstractmethod
from typing import Any


"""
LosBaseCrawler 是一个抽象基类
定义了爬虫的基本结构和接口
"""
class LosBaseCrawler(ABC):
    def __init__(
        self,
        url: str,
        timeout: int = 10
        ) -> None:
        
        self.L_url:str = url
        self.L_timeout:int = timeout
        


        
    """
    获取数据
    """
    @abstractmethod
    def _Lf_fetch(self) -> Any:
        pass
    
    
    
    """
    解析    
    """
    @abstractmethod
    def _Lf_parse(self,data:Any) -> Any:
        pass
    
    
    
    """
    这个方法是爬虫的主方法    
    """
    def Lf_run(self) -> Any:
        raw_data = self._Lf_fetch()
        res = self._Lf_parse(raw_data)
        return res
    
from apscheduler.schedulers.background import BackgroundScheduler
from core.LosConfig import (
    BBC_CRAWL_INTERVAL_TIME,
    RMW_CRAWL_INTERVAL_TIME,
    SCHEDULER_RUN_ON_STARTUP,
)
from core.service.LosBBCService import LosBBCService
from core.service.LosRMWService import LosRMWService

class LosScheduler:
    
    def __init__(self) -> None:
        self.L_scheduler = BackgroundScheduler()
        
    def Lf_run(self):
        self.L_scheduler.add_job(
            func=self._Lf_crawl_bbc,
            trigger="interval",
            minutes = BBC_CRAWL_INTERVAL_TIME,
            id="bbc_crawl_job",
            replace_existing=True
        )
        self.L_scheduler.add_job(
            func=self._Lf_crawl_rmw,
            trigger="interval",
            minutes = RMW_CRAWL_INTERVAL_TIME,
            id = "rmw_crawl_job",
            replace_existing=True
        )
        self.L_scheduler.start()
        print("[LosScheduler] 调度器已经启动 ... ");
        
        if SCHEDULER_RUN_ON_STARTUP:
            self._Lf_crawl_bbc()
            self._Lf_crawl_rmw()
    
    
    """
    public tool
    
    结束定时任务
    """
    def Lf_close(self):
        self.L_scheduler.shutdown(wait=True)
        print("[LosScheduler] 调度器已经关闭")
    
    
    
    """
    private tool get
    
    爬取bbc 信息
    """
    def _Lf_crawl_bbc(self):
        print("[LosScheduler] bbc crawl...")
        try:
            service = LosBBCService()
            res = service.Lf_save_to_db()
            print("[LosScheduler] bbc crawl done\n"
                  f"crawl_number : {res['crawl_number']}\n"
                  f"insert_number : {res['insert_number']}\n"
                  f"ignore_number : {res['ignore_number']}\n"
                  f"total_number : {res['total_number']}\n"
            )
            
        except Exception as e:
            print(f"[LosScheduler] Err: {e}")
            
    
    
    """
    private tool
    
    爬取人民网 信息    
    """
    def _Lf_crawl_rmw(self):
        print("[LosScheduler] rmw crawl...")
        try:
            service = LosRMWService()
            res = service.Lf_save_to_db()
            print("[LosScheduler] rmw crawl done\n"
                  f"crawl_number : {res['crawl_number']}\n"
                  f"insert_number : {res['insert_number']}\n"
                  f"ignore_number : {res['ignore_number']}\n"
                  f"total_number : {res['total_number']}\n"
            )
            
        except Exception as e:
            print(f"[LosScheduler] Err: {e}")
            



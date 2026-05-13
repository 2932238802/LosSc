from fastapi import FastAPI
from core.router.LosCrawlerRouter import LosCrawlerRouter
from core.router.LosNewsRouter import LosNewsRouter
from contextlib import asynccontextmanager
from core.scheduler.LosScheduler import LosScheduler
from core.LosConfig import SCHEDULER_OPEN

L_scheduler: LosScheduler | None = None
@asynccontextmanager
async def lifespan(app:FastAPI):
    global L_scheduler
    print("[LosApp] 启动中...")
    
    if SCHEDULER_OPEN:
        L_scheduler = LosScheduler()
        L_scheduler.Lf_run()
    else:
        print("[LosApp] 定时任务没有开启")
    print("[LosApp] 服务启动成功...")
    
    yield
    
    print("[LosApp] 服务关闭中...")
    if L_scheduler is not None:
        L_scheduler.Lf_close()
    print("[LosApp] 服务已关闭")
        

# 内部会 调用这个 lifespan
app = FastAPI(
    title="LosSc",
    version="0.02",
    description="los scraw api",
    lifespan=lifespan
)


"""
根节点
"""
@app.get("/")
def root():
    return {
        "message": "Hello World"
    }


app.include_router(LosCrawlerRouter)
app.include_router(LosNewsRouter)

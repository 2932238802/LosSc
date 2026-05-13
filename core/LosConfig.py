from pathlib import Path

# __file__ 表示当前文件自己的路径
# resolve 转成 绝对路径 并 解析符号链接
PROJECT_PATH = Path(__file__).resolve().parent.parent

# 数据库 文件夹 以及 数据库的路径
DATA_DIR = PROJECT_PATH / "data"
DB_PATH = DATA_DIR / "los_news.db"

# 是不是开启 定时任务
SCHEDULER_OPEN = False
BBC_CRAWL_INTERVAL_TIME = 10
RMW_CRAWL_INTERVAL_TIME = 15 
SCHEDULER_RUN_ON_STARTUP = True # 这个就是 是不是 启动的时候 就要抓取一次

# BBC
BBC_NEWS_NAME = "BBC"
BBC_NEWS_TIME_OUT = 10
BBC_NEWS_CHANNELS = [
    {"column_name" : "top" , "url" : "https://feeds.bbci.co.uk/news/rss.xml"},
    {"column_name" : "world" , "url" : "https://feeds.bbci.co.uk/news/world/rss.xml"},
    {"column_name" : "business" , "url" : "https://feeds.bbci.co.uk/news/business/rss.xml"},
    {"column_name" : "technology" , "url" : "https://feeds.bbci.co.uk/news/technology/rss.xml"},
    {"column_name" : "sport" , "url" : "https://feeds.bbci.co.uk/sport/rss.xml"},
]

# 人民网 - RenMinWang  RMW
RMW_NEWS_NAME = "RMW"
RMW_NEWS_TIME_OUT = 10
RMW_NEWS_CHANNELS = [
    {"column_name": "ywkx", "url": "http://www.people.com.cn/rss/ywkx.xml"},
]
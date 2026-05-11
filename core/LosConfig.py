from pathlib import Path

# __file__ 表示当前文件自己的路径
# resolve 转成 绝对路径 并 解析符号链接
PROJECT_PATH = Path(__file__).resolve().parent.parent

# 数据库 文件夹 以及 数据库的路径
DATA_DIR = PROJECT_PATH / "data"
DB_PATH = DATA_DIR / "los_news.db"

# rss
BBC_NEWS_URL = "https://feeds.bbci.co.uk/news/rss.xml"
BBC_NEWS_TIME_OUT = 10

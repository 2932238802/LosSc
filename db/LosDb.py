import sqlite3 
from typing import List,Dict,Any
from LosConfig import DB_PATH,DATA_DIR

class LosDb:

    """
    init
    
    初始化
    """
    def __init__(self) -> None:
        DATA_DIR.mkdir(parents=True,exist_ok=True)
        
        # 当前打开的数据库文件
        # 当前事务状态
        # 提交与回滚
        # 创建 cursor
        # 连接级别配置
        # 关闭数据库连接
        self.L_conn : sqlite3.Connection = sqlite3.connect(DB_PATH)
                
        # 这里 要把 本来返回的 
        self.L_conn.row_factory = sqlite3.Row
        
        # 接收 SQL 字符串
        # 将 SQL 交给 SQLite 编译
        # 绑定 SQL 参数
        # 执行 SQL
        # 保存查询结果的读取状态
        # 用 fetchone() / fetchall() 取结果
        self.L_cursor : sqlite3.Cursor = self.L_conn.cursor()
        
        # 初始化一下表
        self._Lf_init_db()
        
        
    """
    init
    
    with工具    
    """
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        self.Lf_close_db()
        # 这里return False 的意思就是 如果with失败了 就要继续抛出异常 
        return False
        
        
        
    """
    init
    
    初始化数据库    
    summary 新闻摘要
    published 发布时间
    source 新闻来源
    """
    def _Lf_init_db(self):
        self.L_cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            summary TEXT,
            published TEXT,
            source TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.L_conn.commit()



    """
    public tool 
    """
    def Lf_get_latest_news_db(
        self,
        limit:int = 20,
    ) -> List[Any]:
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,source,created_at
            FROM news
            ORDER BY id DESC
            LIMIT ?            
            """
            ,
            # tuple 
            # 单个参数的 tuple 必须写成 (limit,)
            # 如果写成 (limit)，只是普通括号表达式
            (limit,)
        )        
        rows = self.L_cursor.fetchall()
        return [dict(row) for row in rows]


    """
    public tool
    """
    def Lf_get_count(self):
        # COUNT(*) 返回结果类似 (35,)
        self.L_cursor.execute("""
                              SELECT COUNT(*)
                              FROM news
                              """);
        row = self.L_cursor.fetchone()
        return row[0]    




    """
    public tool    
    """
    def Lf_close_db(self):
        self.L_conn.close()
        
    
    
    """
    public tool
    
    插入数据 
    """
    def Lf_insert_news_db(
        self,
        title:str,
        link:str,
        summary:str = '',
        published:str ='',
        source:str = ''
    ) -> bool:
        # IGNORE 就是插入重复的时候 不要报错
        self.L_cursor.execute(
        """
        INSERT OR IGNORE INTO news(
            title,
            link,
            summary,
            published,
            source                
        )
        VALUES (?, ?, ?, ?, ?)
        """
        , 
        (title, link, summary, published, source))
        self.L_conn.commit()
        
        return self.L_cursor.rowcount == 1
    
        
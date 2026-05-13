import sqlite3 
from typing import List,Dict,Any
from core.LosConfig import DB_PATH,DATA_DIR

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
    news_name 新闻网站名字，例如 BBC / RMW
    column_name 新闻网站下的栏目，例如 top / xwyk / world
    """
    def _Lf_init_db(self):
        self.L_cursor.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            link TEXT NOT NULL UNIQUE,
            summary TEXT,
            published TEXT,
            news_name TEXT,
            column_name TEXT,
            image_url TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.L_conn.commit()



    """
    public tool get
    """
    def Lf_get_latest_news(
        self,
        limit:int = 20,
    ) -> List[Dict[str,Any]]:
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,news_name,column_name,image_url,created_at
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
    public tool get
    - 
    """
    def Lf_get_latest_news_by_page(
        self,
        page:int = 1,
        page_size:int = 20
    ) -> List[Dict[str,Any]]:
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 20
            
        offset = (page - 1) * page_size
        
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,news_name,column_name,image_url,created_at
            FROM news
            ORDER BY id DESC            
            LIMIT ?
            OFFSET ?
            """
            ,
            (page_size,offset,)
        )
        
        # 和 commit 不同
        # commit 会修改表的结构
        rows = self.L_cursor.fetchall()
        return [dict(row) for row in rows]



    """
    public tool get
    
    获取指定新闻网站的最新新闻
    """
    def Lf_get_latest_news_by_news_name(
        self,
        news_name: str,
        limit:int = 20
    ) -> List[Dict[str,Any]]:
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,news_name,column_name,image_url,created_at
            FROM news
            WHERE news_name = ?
            ORDER BY id DESC
            LIMIT ?            
            """
            ,
            (news_name, limit,)
        )        
        rows = self.L_cursor.fetchall()
        return [dict(row) for row in rows]



    """
    public tool get
    
    分页获取指定新闻网站的新闻
    """
    def Lf_get_latest_news_by_news_name_and_page(
        self,
        news_name: str,
        page:int = 1,
        page_size:int = 20
    )-> List[Dict[str,Any]]:
        if page < 1 :
            page = 1
        if page_size < 1:
            page_size = 20
        
        offset = (page - 1) * page_size
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,news_name,column_name,image_url,created_at
            FROM news
            WHERE news_name = ?
            ORDER BY id DESC            
            LIMIT ?
            OFFSET ?
            """
            ,
            (news_name,page_size,offset,)
        )
        rows = self.L_cursor.fetchall()
        return [dict(row) for row in rows]



    """
    public tool get
    
    分页获取指定新闻网站下指定栏目的新闻
    """
    def Lf_get_latest_news_by_news_name_and_column_name_and_page(
        self,
        news_name: str,
        column_name: str,
        page:int = 1,
        page_size:int = 20
    )-> List[Dict[str,Any]]:
        if page < 1 :
            page = 1
        if page_size < 1:
            page_size = 20
        
        offset = (page - 1) * page_size
        self.L_cursor.execute(
            """
            SELECT id,title,link,summary,published,news_name,column_name,image_url,created_at
            FROM news
            WHERE news_name = ? AND column_name = ?
            ORDER BY id DESC            
            LIMIT ?
            OFFSET ?
            """
            ,
            (news_name,column_name,page_size,offset,)
        )
        rows = self.L_cursor.fetchall()
        return [dict(row) for row in rows]



    """
    public tool get
    获取 新闻网站列表
    """
    def Lf_get_news_names(self) -> List[str]:
        self.L_cursor.execute(
            """
            SELECT DISTINCT news_name
            FROM news
            WHERE news_name IS NOT NULL AND news_name != ''
            ORDER BY news_name ASC            
            """
        )
        rows = self.L_cursor.fetchall()
        return [row["news_name"] for row in rows]



    """
    public tool get
    
    获取指定新闻网站下的栏目列表
    """
    def Lf_get_column_names_by_news_name(self,news_name:str) -> List[str]:
        self.L_cursor.execute(
            """
            SELECT DISTINCT column_name
            FROM news
            WHERE news_name = ? AND column_name IS NOT NULL AND column_name != ''
            ORDER BY column_name ASC            
            """
            ,
            (news_name,)
        )
        rows = self.L_cursor.fetchall()
        return [row["column_name"] for row in rows]



    """
    public tool get
    """
    def Lf_get_count(self) -> int:
        # COUNT(*) 返回结果类似 (35,)
        self.L_cursor.execute("""
                              SELECT COUNT(*)
                              FROM news
                              """);
        row = self.L_cursor.fetchone()
        return row[0]    



    """
    public tool get
    获取 指定新闻网站的新闻个数
    """
    def Lf_get_count_by_news_name(self,news_name:str) -> int:
        self.L_cursor.execute(
            """
            SELECT COUNT(*)
            FROM news
            WHERE news_name = ?            
            """
            ,
            (news_name,)
        )
        res = self.L_cursor.fetchone()
        return res[0]    



    """
    public tool get
    获取 指定新闻网站下指定栏目的新闻个数
    """
    def Lf_get_count_by_news_name_and_column_name(self,news_name:str,column_name:str) -> int:
        self.L_cursor.execute(
            """
            SELECT COUNT(*)
            FROM news
            WHERE news_name = ? AND column_name = ?            
            """
            ,
            (news_name,column_name,)
        )
        res = self.L_cursor.fetchone()
        return res[0]    



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
        news_name:str = '',
        column_name:str = '',
        image_url:str = ''
    ) -> bool:
        # IGNORE 就是插入重复的时候 不要报错
        self.L_cursor.execute(
        """
        INSERT OR IGNORE INTO news(
            title,
            link,
            summary,
            published,
            news_name,
            column_name,
            image_url                
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        , 
        (title, link, summary, published, news_name,column_name,image_url))
        self.L_conn.commit()
        
        return self.L_cursor.rowcount == 1
    
    
        
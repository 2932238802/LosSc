# LosSc API 文档

本文档记录 LosSc 当前已经提供的 HTTP API。

## 当前接口列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 根接口，用于测试服务是否运行 |
| GET | `/api/news/bbc/latest` | 从数据库中获取 BBC 最新新闻 |
| GET | `/api/news/bbc/bypage` | 分页获取 BBC 新闻列表 |
| POST | `/api/crawler/bbc` | 手动触发 BBC RSS 新闻抓取并入库 |

---

## 1. 根接口

### `GET /`

用于测试服务器是否正常运行。

### 请求参数

无。

### 响应示例

```json
{
  "message": "Hello World"
}
```

---

## 2. 获取 BBC 最新新闻

### `GET /api/news/bbc/latest`

从 SQLite 数据库中获取 BBC 最新新闻列表。

### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `limit` | `int` | `10` | 返回的新闻数量 |

### 请求示例

```http
GET /api/news/bbc/latest?limit=3
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | `bool` | 请求是否成功 |
| `message` | `string` | 响应说明 |
| `data.count` | `int` | 返回新闻数量 |
| `data.items` | `array` | 新闻列表 |
| `data.items[].id` | `int` | 数据库新闻 ID |
| `data.items[].title` | `string` | 新闻标题 |
| `data.items[].link` | `string` | 新闻链接 |
| `data.items[].summary` | `string` | 新闻摘要 |
| `data.items[].published` | `string` | 新闻发布时间，来自 RSS 源 |
| `data.items[].source` | `string` | 新闻来源 |
| `data.items[].image_url` | `string` | 新闻封面图地址，当前可能为空字符串 |
| `data.items[].created_at` | `string` | 数据入库时间 |

### 响应示例

```json
{
  "success": true,
  "message": "latest news fetched",
  "data": {
    "count": 3,
    "items": [
      {
        "id": 1,
        "title": "新闻标题",
        "link": "https://example.com/news",
        "summary": "新闻摘要",
        "published": "Mon, 11 May 2026 08:00:00 GMT",
        "source": "BBC",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 3. 分页获取 BBC 新闻

### `GET /api/news/bbc/bypage`

分页从 SQLite 数据库中获取 BBC 新闻列表。

### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `page` | `int` | `1` | 页码，从 1 开始，必须 `>= 1` |
| `page_size` | `int` | `20` | 每页返回的新闻数量，范围 `1 <= page_size <= 100` |

### 请求示例

```http
GET /api/news/bbc/bypage?page=1&page_size=20
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | `bool` | 请求是否成功 |
| `message` | `string` | 响应说明 |
| `data.page` | `int` | 当前页码 |
| `data.page_size` | `int` | 每页新闻数量 |
| `data.total_number` | `int` | 数据库中的新闻总数量 |
| `data.total_page` | `int` | 总页数 |
| `data.has_next` | `bool` | 是否存在下一页 |
| `data.has_prev` | `bool` | 是否存在上一页 |
| `data.items` | `array` | 当前页新闻列表 |
| `data.items[].id` | `int` | 数据库新闻 ID |
| `data.items[].title` | `string` | 新闻标题 |
| `data.items[].link` | `string` | 新闻链接 |
| `data.items[].summary` | `string` | 新闻摘要 |
| `data.items[].published` | `string` | 新闻发布时间，来自 RSS 源 |
| `data.items[].source` | `string` | 新闻来源 |
| `data.items[].image_url` | `string` | 新闻封面图地址，当前可能为空字符串 |
| `data.items[].created_at` | `string` | 数据入库时间 |

### 响应示例

```json
{
  "success": true,
  "message": "news page fetched",
  "data": {
    "page": 1,
    "page_size": 20,
    "total_number": 120,
    "total_page": 6,
    "has_next": true,
    "has_prev": false,
    "items": [
      {
        "id": 1,
        "title": "新闻标题",
        "link": "https://example.com/news",
        "summary": "新闻摘要",
        "published": "Mon, 11 May 2026 08:00:00 GMT",
        "source": "BBC",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 4. 手动抓取 BBC 新闻

### `POST /api/crawler/bbc`

手动触发 BBC RSS 新闻抓取，并写入 SQLite 数据库。

重复新闻会根据 `link` 字段去重。

### 请求参数

无。

### 请求示例

```http
POST /api/crawler/bbc
```

### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `success` | `bool` | 请求是否成功 |
| `message` | `string` | 响应说明 |
| `data.crawl_number` | `int` | 本次从 RSS 抓取到的新闻数量 |
| `data.insert_number` | `int` | 本次新插入数据库的新闻数量 |
| `data.ignore_number` | `int` | 本次因重复而忽略的新闻数量 |
| `data.total_number` | `int` | 当前数据库中的新闻总数量 |

### 响应示例

```json
{
  "success": true,
  "message": "BBC news crawl finished",
  "data": {
    "crawl_number": 30,
    "insert_number": 2,
    "ignore_number": 28,
    "total_number": 120
  }
}
```

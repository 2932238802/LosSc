# LosSc API 文档

本文档记录 LosSc 当前已经提供的 HTTP API。

**服务地址**
- 本地开发：`http://127.0.0.1:8000`
- 部署（阿里云）：`http://47.98.163.222:8000`

**统一响应格式**

所有接口都返回统一结构的 JSON：

```json
{
  "success": true,
  "message": "...",
  "data": { ... }
}
```

- `success`：`bool`，请求是否成功
- `message`：`string`，说明信息
- `data`：`object`，接口数据，结构因接口而异

---

## 数据模型

### 新闻 news

数据库中每条新闻包含的核心字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | `int` | 数据库自增主键 |
| `title` | `string` | 新闻标题 |
| `link` | `string` | 新闻链接，全库唯一 |
| `summary` | `string` | 新闻摘要 |
| `published` | `string` | 新闻发布时间，来自 RSS 源，格式与源站保持一致 |
| `news_name` | `string` | 所属新闻网站，英文标识，例如 `BBC` / `RMW` |
| `column_name` | `string` | 所属栏目，英文标识，例如 `top` / `ywkx` |
| `image_url` | `string` | 新闻封面图地址，当前可能为空字符串 |
| `created_at` | `string` | 数据入库时间 |

### 当前已支持的新闻源

| `news_name` | 含义 | `column_name` | 栏目说明 | RSS 源 |
|---|---|---|---|---|
| `BBC` | BBC News | `top` | 头条 | `https://feeds.bbci.co.uk/news/rss.xml` |
| `RMW` | 人民网（RenMinWang）| `ywkx` | 要闻快讯 | `http://www.people.com.cn/rss/ywkx.xml` |

---

## 接口列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/` | 根接口，测试服务是否运行 |
| GET | `/api/news/latest` | 获取最新新闻（混合流） |
| GET | `/api/news/bypage` | 分页获取新闻（混合流） |
| GET | `/api/news/news_names` | 获取新闻网站列表 |
| GET | `/api/news/columns` | 获取指定新闻网站下的栏目列表 |
| GET | `/api/news/by_news_name/bypage` | 按新闻网站分页获取新闻 |
| GET | `/api/news/by_news_name_and_column/bypage` | 按新闻网站 + 栏目分页获取新闻 |
| POST | `/api/crawler/bbc` | 手动触发 BBC 抓取并入库 |
| POST | `/api/crawler/rmw` | 手动触发 人民网 抓取并入库 |

---

## 1. 根接口

### `GET /`

用于测试服务器是否正常运行。

#### 请求参数

无。

#### 响应示例

```json
{
  "message": "Hello World"
}
```

> 注：此接口返回的是简单的 JSON，没有走统一的 `success/message/data` 结构。

---

## 2. 获取最新新闻（混合流）

### `GET /api/news/latest`

从 SQLite 数据库中按 `id DESC` 获取最新新闻，不区分来源，用于「快捷信息」页面。

#### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `limit` | `int` | `10` | 返回的新闻数量，范围 `1 <= limit <= 100` |

#### 请求示例

```http
GET /api/news/latest?limit=3
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.count` | `int` | 返回新闻数量 |
| `data.items` | `array` | 新闻列表，元素结构见「数据模型 - news」 |

#### 响应示例

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
        "news_name": "BBC",
        "column_name": "top",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 3. 分页获取新闻（混合流）

### `GET /api/news/bypage`

分页从 SQLite 数据库中获取全部新闻（混合流，按 `id DESC`），用于手机端「快捷信息」页面的滚动加载。

#### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `page` | `int` | `1` | 页码，必须 `>= 1` |
| `page_size` | `int` | `20` | 每页新闻数量，范围 `1 <= page_size <= 100` |

#### 请求示例

```http
GET /api/news/bypage?page=1&page_size=20
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.page` | `int` | 当前页码 |
| `data.page_size` | `int` | 每页新闻数量 |
| `data.total_number` | `int` | 数据库中的新闻总数量 |
| `data.total_page` | `int` | 总页数 |
| `data.has_next` | `bool` | 是否存在下一页 |
| `data.has_prev` | `bool` | 是否存在上一页 |
| `data.items` | `array` | 当前页新闻列表 |

#### 响应示例

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
        "id": 120,
        "title": "新闻标题",
        "link": "https://example.com/news",
        "summary": "新闻摘要",
        "published": "Mon, 11 May 2026 08:00:00 GMT",
        "news_name": "BBC",
        "column_name": "top",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 4. 获取新闻网站列表

### `GET /api/news/news_names`

获取当前数据库中已经存在的 **新闻网站** 列表，用于手机端「首页」展示有哪些可选的新闻源。

#### 请求参数

无。

#### 请求示例

```http
GET /api/news/news_names
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.count` | `int` | 新闻网站数量 |
| `data.items` | `array<string>` | 新闻网站名称列表（`news_name`） |

#### 响应示例

```json
{
  "success": true,
  "message": "news names fetched",
  "data": {
    "count": 2,
    "items": [
      "BBC",
      "RMW"
    ]
  }
}
```

---

## 5. 获取指定新闻网站下的栏目列表

### `GET /api/news/columns`

获取某个新闻网站下，数据库中已存在的栏目列表，用于手机端进入某个网站后展示「所有栏目」。

#### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `news_name` | `string` | 必填 | 新闻网站，例如 `BBC` |

#### 请求示例

```http
GET /api/news/columns?news_name=BBC
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.news_name` | `string` | 查询的新闻网站 |
| `data.count` | `int` | 栏目数量 |
| `data.items` | `array<string>` | 栏目名称列表（`column_name`） |

#### 响应示例

```json
{
  "success": true,
  "message": "column names fetched",
  "data": {
    "news_name": "BBC",
    "count": 1,
    "items": [
      "top"
    ]
  }
}
```

---

## 6. 按新闻网站分页获取新闻

### `GET /api/news/by_news_name/bypage`

按 `news_name` 分页从数据库获取新闻，用于在手机端查看「某个新闻网站下所有栏目的新闻」。

#### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `news_name` | `string` | 必填 | 新闻网站，例如 `BBC` |
| `page` | `int` | `1` | 页码，必须 `>= 1` |
| `page_size` | `int` | `20` | 每页新闻数量，范围 `1 <= page_size <= 50` |

#### 请求示例

```http
GET /api/news/by_news_name/bypage?news_name=BBC&page=1&page_size=20
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.news_name` | `string` | 查询的新闻网站 |
| `data.page` | `int` | 当前页码 |
| `data.page_size` | `int` | 每页新闻数量 |
| `data.total_number` | `int` | 当前 `news_name` 下的新闻总数量 |
| `data.total_page` | `int` | 总页数 |
| `data.has_next` | `bool` | 是否存在下一页 |
| `data.has_prev` | `bool` | 是否存在上一页 |
| `data.items` | `array` | 当前页新闻列表 |

#### 响应示例

```json
{
  "success": true,
  "message": "news_name page fetched",
  "data": {
    "news_name": "BBC",
    "page": 1,
    "page_size": 20,
    "total_number": 34,
    "total_page": 2,
    "has_next": true,
    "has_prev": false,
    "items": [
      {
        "id": 34,
        "title": "新闻标题",
        "link": "https://example.com/news",
        "summary": "新闻摘要",
        "published": "Mon, 11 May 2026 08:00:00 GMT",
        "news_name": "BBC",
        "column_name": "top",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 7. 按新闻网站 + 栏目分页获取新闻

### `GET /api/news/by_news_name_and_column/bypage`

按 `news_name` + `column_name` 同时过滤并分页，用于手机端查看「某个网站下具体某个栏目的新闻」。

#### Query 参数

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `news_name` | `string` | 必填 | 新闻网站，例如 `BBC` |
| `column_name` | `string` | 必填 | 栏目，例如 `top` |
| `page` | `int` | `1` | 页码，必须 `>= 1` |
| `page_size` | `int` | `20` | 每页新闻数量，范围 `1 <= page_size <= 50` |

#### 请求示例

```http
GET /api/news/by_news_name_and_column/bypage?news_name=BBC&column_name=top&page=1&page_size=20
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.news_name` | `string` | 查询的新闻网站 |
| `data.column_name` | `string` | 查询的栏目 |
| `data.page` | `int` | 当前页码 |
| `data.page_size` | `int` | 每页新闻数量 |
| `data.total_number` | `int` | 该网站 + 栏目下的新闻总数量 |
| `data.total_page` | `int` | 总页数 |
| `data.has_next` | `bool` | 是否存在下一页 |
| `data.has_prev` | `bool` | 是否存在上一页 |
| `data.items` | `array` | 当前页新闻列表 |

#### 响应示例

```json
{
  "success": true,
  "message": "news_name and column_name page fetched",
  "data": {
    "news_name": "BBC",
    "column_name": "top",
    "page": 1,
    "page_size": 20,
    "total_number": 30,
    "total_page": 2,
    "has_next": true,
    "has_prev": false,
    "items": [
      {
        "id": 30,
        "title": "新闻标题",
        "link": "https://example.com/news",
        "summary": "新闻摘要",
        "published": "Mon, 11 May 2026 08:00:00 GMT",
        "news_name": "BBC",
        "column_name": "top",
        "image_url": "",
        "created_at": "2026-05-11 10:00:00"
      }
    ]
  }
}
```

---

## 8. 手动抓取 BBC 新闻

### `POST /api/crawler/bbc`

手动触发 BBC RSS 新闻抓取，并写入 SQLite 数据库。

- 抓取的新闻会写入：`news_name = "BBC"`，`column_name = "top"`
- 重复新闻根据 `link` 字段去重（数据库层面用 `UNIQUE` 约束 + `INSERT OR IGNORE`）

#### 请求参数

无。

#### 请求示例

```http
POST /api/crawler/bbc
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.crawl_number` | `int` | 本次从 RSS 抓取到的新闻数量 |
| `data.insert_number` | `int` | 本次新插入数据库的新闻数量 |
| `data.ignore_number` | `int` | 本次因 `link` 重复而忽略的新闻数量 |
| `data.total_number` | `int` | 当前数据库中的新闻总数量 |

#### 响应示例

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

---

## 9. 手动抓取 人民网 新闻

### `POST /api/crawler/rmw`

手动触发 **人民网 要闻快讯** RSS 新闻抓取，并写入 SQLite 数据库。

- 抓取的新闻会写入：`news_name = "RMW"`，`column_name = "ywkx"`
- 重复新闻根据 `link` 字段去重（数据库层面用 `UNIQUE` 约束 + `INSERT OR IGNORE`）

#### 请求参数

无。

#### 请求示例

```http
POST /api/crawler/rmw
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|---|---|---|
| `data.crawl_number` | `int` | 本次从 RSS 抓取到的新闻数量 |
| `data.insert_number` | `int` | 本次新插入数据库的新闻数量 |
| `data.ignore_number` | `int` | 本次因 `link` 重复而忽略的新闻数量 |
| `data.total_number` | `int` | 当前数据库中的新闻总数量 |

#### 响应示例

```json
{
  "success": true,
  "message": "RMW news crawl finished",
  "data": {
    "crawl_number": 20,
    "insert_number": 5,
    "ignore_number": 15,
    "total_number": 140
  }
}
```

---

## 失败响应

所有接口在失败时都会返回如下统一格式：

```json
{
  "success": false,
  "message": "错误原因说明",
  "data": null
}
```

---

## 典型调用流程（以手机端为例）

1. 进入首页 → `GET /api/news/news_names` 拿到「BBC / RMW」列表
2. 点击某个网站（例如 BBC）→ `GET /api/news/columns?news_name=BBC` 拿到该网站的栏目列表
3. 进入栏目 → `GET /api/news/by_news_name_and_column/bypage?news_name=BBC&column_name=top&page=1&page_size=20`
4. 或者直接进入「快捷信息」混合流页面 → `GET /api/news/bypage?page=1&page_size=20`
5. 后台/管理端手动触发抓取 → `POST /api/crawler/bbc` 或 `POST /api/crawler/rmw`

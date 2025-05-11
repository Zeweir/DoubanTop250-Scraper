# 🕸️ DoubanTop250-Scraper

一个简单易用的豆瓣 Top250 页面爬虫工具，包含数据抓取与结构化解析功能。支持用户自定义参数配置，方便适配不同网页结构或需求。

---

## 📦 功能概览

### main.py - 数据抓取
- ✅ 自动分页抓取豆瓣 Top250 页面
- ✅ 支持模拟浏览器请求头（Headers）和 Cookie
- ✅ 每页数据压缩成一行，保存为 [.txt](file://E:\pythonproject\myspider2Douban\inputdata\doubantop250.txt) 文件
- ✅ 可配置：分页步长、页面数量、请求间隔等参数

### extract.py - 数据解析
- ✅ 解析抓取到的 HTML 内容，提取电影信息
- ✅ 输出结构化 JSON 格式文件
- ✅ 支持字段：
  - 标题、副标题
  - 导演、年份、国家、类型
  - 评分、评论人数、引言描述
- ✅ 支持中文字符处理，自动创建输出目录

---

## ⚙️ 可配置参数说明

### main.py 中可修改参数

| 参数名                                                       | 含义                                |
| ------------------------------------------------------------ | ----------------------------------- |
| [URL]                                                        | 要抓取的目标网址                    |
| [HEADERS]/ [COOKIES]                                         | 请求头和 Cookie，用于伪装浏览器访问 |
| [START_STEP]/ [PAGE_COUNT]                                   | 分页参数，控制抓取多少页            |
| [INPUT_DIR]/ [OUTPUT_FILENAME] | 输入目录和输出文件名                |
| [REQUEST_TIMEOUT] / [REQUEST_INTERVAL] | 请求超时时间和请求间隔              |

### extract.py 中可修改参数

| 参数                                                         | 含义                                              |
| ------------------------------------------------------------ | ------------------------------------------------- |
| [INPUT_FILE_PATH] | 存放原始 HTML 数据的文件路径                      |
| [OUTPUT_FILE_PATH] | 输出 JSON 文件路径                                |
| `XPATH_*`                                                    | 提取电影信息的 XPath 表达式（可根据页面结构调整） |

---

## 🧰 使用方法

### 1. 安装依赖

```bash
pip install requests tqdm lxml
```


### 2. 抓取豆瓣 Top250 页面数据

运行 [main.py] 开始抓取：

```bash
python main.py
```


抓取结果将保存在 `inputdata/doubantop250.txt` 中，每行对应一页内容。

### 3. 解析 HTML 数据并生成 JSON

运行 [extract.py] 进行数据解析：

```bash
python extract.py
```


解析结果将保存在 `outputdata/doubantop250.json` 中，格式为结构化的电影信息列表。

---

## 📁 目录结构建议

```
DoubanTop250-Scraper/
├── main.py              # 爬虫脚本
├── extract.py           # 数据解析脚本
├── inputdata/           # 存放抓取的 HTML 数据
├── outputdata/          # 存放解析后的 JSON 数据
└── README.md            # 项目说明文档
```


---

## 📝 示例输出 JSON 片段

```json
[
  {
    "title": "肖申克的救赎",
    "other_titles": ["The Shawshank Redemption"],
    "director": "弗兰克·德拉邦特",
    "year": "1994",
    "country": "美国",
    "genre": ["剧情", "励志"],
    "score": "9.7",
    "comments": "2864923",
    "quote": "希望是美好的，也许是人间至善，而美好的事物永不消逝。"
  },
  ...
]
```


---

## 📌 注意事项

- 抓取频率请适当控制（默认 `REQUEST_INTERVAL = 1s`），避免触发反爬机制。
- 如需适配其他网站，请修改对应的 URL 和 XPath 配置。

---

## 🤝 贡献指南

欢迎提交 PR 或 issue，共同完善此项目！你可以尝试：
- 添加代理 IP 支持
- 实现多线程/异步抓取
- 增加日志记录功能
- 将数据导出为 CSV 或数据库格式

---

## 📄 License

MIT License


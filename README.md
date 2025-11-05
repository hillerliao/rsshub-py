# RSSHub-Py

一个简单高效的RSS生成服务，使用Python Flask框架开发。该项目支持从多个内容源（电子杂志、新闻、科技文章、博客等）抓取内容并生成标准的RSS订阅源。

## 功能特性

- **多源聚合**：支持多种内容源的RSS生成
- **标准格式**：生成符合规范的RSS 2.0格式内容
- **智能缓存**：内置文件系统缓存机制，提高访问速度
- **易于扩展**：模块化设计，方便添加新的内容源
- **响应式UI**：美观的Web界面，支持各种设备访问
- **多方式部署**：支持本地、Docker和Vercel部署

## 项目结构

```
app/
├── __init__.py      # 应用初始化
├── routes.py        # 路由定义
├── core/            # 核心功能
│   ├── __init__.py
│   ├── rss_generator.py  # RSS生成器
│   └── cache.py     # 缓存系统
├── spiders/         # 内容爬虫
│   ├── __init__.py
│   ├── base_spider.py    # 基础爬虫类
│   └── emagazine.py      # 电子杂志爬虫
└── templates/       # HTML模板
    └── index.html   # 首页模板
requirements.txt     # 项目依赖
vercel.json          # Vercel部署配置
main.py              # 应用入口
config.py            # 配置文件
runtime.txt          # Python版本指定
```

## 安装与运行

### 本地开发环境

1. 克隆项目

```bash
git clone https://github.com/yourusername/rsshub-py.git
cd rsshub-py
```

2. 创建虚拟环境

```bash
python -m venv venv
# Windows
env\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. 安装依赖

```bash
pip install -r requirements.txt
```

4. 运行应用

```bash
python main.py
```

5. 访问应用

打开浏览器访问 http://localhost:5000

### 使用Docker部署

1. 确保已安装Docker和Docker Compose

2. 构建并启动容器

```bash
docker-compose up -d
```

3. 访问应用

打开浏览器访问 http://localhost:5000

### 部署到Vercel

1. Fork本仓库到你的GitHub账号

2. 在 [Vercel](https://vercel.com) 注册账号并连接GitHub

3. 导入你的仓库并点击部署

4. 部署完成后，Vercel会提供一个URL供你访问

## API使用说明

### 获取RSS源

```
GET /emagazine
```

**示例：**
```
GET /emagazine
```

### 健康检查

```
GET /health
```

### 获取所有可用源

```
GET /api/sources
```

**返回示例：**
```json
{
  "sources": ["emagazine", "news", "tech", "blog"]
}
```

### 健康检查

```
GET /health
```

## 添加新的内容源

1. 在 `app/spiders/` 目录下创建新的爬虫文件，例如 `mysource.py`

2. 继承 `BaseSpider` 类并实现 `fetch_items()` 方法

```python
from app.spiders.base_spider import BaseSpider

class MySourceSpider(BaseSpider):
    def __init__(self):
        super().__init__(name='mysource')
    
    def fetch_items(self):
        # 实现获取内容的逻辑
        items = []
        # ...
        return items
```

3. 在 `app/spiders/__init__.py` 中导出新的爬虫类

4. 在 `app/routes.py` 的 `get_feed()` 函数中添加新的源

## 配置项

可通过环境变量或修改 `config.py` 文件进行配置：

- `SECRET_KEY`：应用密钥，生产环境必须设置
- `DEBUG`：调试模式开关
- `CACHE_DIR`：缓存目录路径
- `DEFAULT_CACHE_TTL`：默认缓存时间（秒）
- `REQUEST_TIMEOUT`：请求超时时间（秒）

## 技术栈

- **后端**：Python 3.12, Flask
- **HTML解析**：BeautifulSoup4, lxml
- **HTTP请求**：requests
- **部署**：Gunicorn (生产环境), Vercel

## 开发注意事项

1. 爬取内容时请遵守相关网站的robots.txt规则和使用条款

2. 对于频繁访问的源，建议调整缓存时间以减轻源网站压力

## 许可证

本项目采用 MIT 许可证 - 详情请查看 [LICENSE](LICENSE) 文件

## 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目！
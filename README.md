# 智能运维前线 — AIOps 每日精选

> 聚合 AIOps / DevOps / SRE 行业动态、开源工具、技术实践，每日早 8:00 自动更新

---

## 项目结构

```
aiops-hot/
├── scripts/
│   ├── config.py          # 数据源配置（RSS源、关键词、工具库）
│   ├── fetch.py           # 核心抓取脚本（RSS + GitHub + 博客）
│   ├── run_daily.bat      # Windows 定时任务入口脚本
│   └── setup_scheduler.py # 计划任务安装脚本
├── site/                   # Hugo 静态站点
│   ├── hugo.toml           # Hugo 配置
│   ├── layouts/            # 模板（首页/列表/详情）
│   ├── static/css/         # 样式文件
│   └── content/            # 内容文件（自动生成）
│       ├── articles/       # 行业动态文章
│       ├── tools/          # 工具库
│       └── daily/          # 每日日报
├── data/
│   └── articles_state.json # 抓取状态（去重记录）
└── README.md
```

---

## 数据来源

### 行业动态（RSS / 博客）
- **InfoQ 中国** — 技术深度文章
- **Red Hat Blog** — DevOps / AIOps 实践
- **SRE Weekly** — 国际 SRE 资讯
- **腾讯云开发者社区** — 大厂实践
- **华为云 / 阿里云** — 智能运维案例

### 开源工具（GitHub API）
按 AIOps/DevOps/SRE 关键词搜索 GitHub，按 Stars 排序收录

### 固定工具库
内置 10 个业界知名 AIOps/DevOps 工具（Keep、Trivy、Thanos、OpenTelemetry Collector 等）

---

## 手动运行

```bash
# 1. 进入目录
cd C:\Users\wangc\.qclaw\workspace\aiops-hot

# 2. 抓取数据 + 构建站点（一条命令）
.\scripts\run_daily.bat

# 或者分开执行：
python scripts/fetch.py          # 抓取数据
hugo -p site                     # 构建站点（site 目录下执行）
```

---

## 本地预览

```bash
cd aiops-hot/site
hugo server --port 1313
# 访问 http://localhost:1313
```

---

## 自动更新（每天早 8:00）

计划任务 `AIOpsHot_DailyUpdate` 已创建，开机登录后自动触发。

**验证计划任务：**
```powershell
SchTasks /Query /TN "AIOpsHot_DailyUpdate" /FO LIST
```

**修改运行时间（如改为 9:00）：**
```powershell
SchTasks /Change /TN "AIOpsHot_DailyUpdate" /ST 09:00
```

**删除计划任务：**
```powershell
SchTasks /Delete /TN "AIOpsHot_DailyUpdate" /F
```

---

## 添加新的 RSS 源

编辑 `scripts/config.py`，在 `RSS_FEEDS` 列表中添加：

```python
{
    "name": "站点名称",
    "url": "RSS地址",
    "category": "practice",  # practice | case | news
    "section": "articles",
    "tags": ["标签1", "标签2"],
    "weight": 8,             # 1-10，权重越高越靠前
},
```

---

## 自定义工具库

编辑 `scripts/config.py` 中的 `FEATURED_TOOLS` 列表添加固定工具。

---

## 部署（可选）

### Vercel（推荐）
1. 将 `site/public` 目录推送到 GitHub
2. 在 Vercel 导入项目，Build Command 填 `hugo`
3. 域名绑定后自动 HTTPS

### 替换数据源
当前脚本使用免费 GitHub API（60次/小时），如需更稳定可申请 Personal Access Token。

---

**最后更新：2026-07-25**

# 智能运维前线 — AIOps 每日精选

> 聚合 AIOps / DevOps / SRE 行业动态、开源工具、技术实践，每日早 8:00 自动更新

**访问地址：** http://zbit.info:8888

---

## 项目结构

```
aiops-hot/
├── .github/
│   └── workflows/
│       └── deploy.yml     # GitHub Actions 自动部署工作流
├── scripts/
│   ├── config.py          # 数据源配置（RSS源、关键词、工具库）
│   ├── fetch.py           # 核心抓取脚本（RSS + GitHub Trending）
│   ├── fetch_feeds.py     # RSS 订阅源抓取
│   ├── fetch_github.py    # GitHub Trending 抓取
│   ├── run_daily.bat      # Windows 定时任务入口脚本
│   ├── setup_scheduler.ps1 # 计划任务 PowerShell 安装脚本
│   └── nginx-aiops-hot.conf # 服务器 nginx 站点配置
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

## 手动运行（抓取数据）

```bash
# 进入目录
cd C:\Users\wangc\.qclaw\workspace\aiops-hot

# 抓取数据（RSS + GitHub Trending）
python scripts/fetch.py

# 本地预览
cd site
hugo server --port 1313
# 访问 http://localhost:1313
```

---

## 自动部署（GitHub Actions）

每次推送到 `main` 分支，GitHub Actions 自动完成：SSH 登录服务器 → 拉取最新代码 → Hugo 重新构建 → 站点上线。整个过程约 **17 秒**。

**部署流程：**
```
git push origin main
    ↓
GitHub Actions (Ubuntu  runner)
    ↓
  1. Checkout 代码
  2. Hugo Extended 0.164.0 构建
  3. SSH 登录 zbit.info
  4. git pull + hugo rebuild
    ↓
站点自动更新 → http://zbit.info:8888
```

**部署密钥：**
- `DEPLOY_KEY` Secret 已配置（服务器 SSH ED25519 私钥）
- 仅允许 git fetch 操作，不支持交互登录
- 部署用户 `ubuntu`，站点目录 `/var/www/aiops-hot`

**查看部署状态：**
```bash
# 最近运行
gh run list --repo bugtest/aiops-hot

# 详细日志
gh run view <run-id> --log --repo bugtest/aiops-hot
```

**触发部署：**
```bash
git add -A
git commit -m "update"
git push origin main
```

---

## 本地定时更新（每天早 8:00）

计划任务 `AIOpsHot_DailyUpdate` 在本地 Windows 运行，抓取数据后自动推送 GitHub 触发 CI/CD。

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

## 服务器信息

| 项目 | 值 |
|------|-----|
| 访问地址 | http://zbit.info:8888 |
| 服务器 | zbit.info |
| SSH 用户 | ubuntu |
| 站点目录 | `/var/www/aiops-hot` |
| nginx 配置 | `/etc/nginx/sites-available/aiops-hot.conf` |
| 构建工具 | Hugo Extended v0.164.0 |
| **注意** | 端口 80 被 Shadowsocks 占用，nginx 使用 8888 端口 |

---

**最后更新：2026-07-25**

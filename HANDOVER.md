# 智能运维前线 — 项目交接文档

**整理时间：** 2026-07-25
**负责人：** QClaw Agent

---

## 一、项目概述

**名称：** 智能运维前线（AIOps Hot）
**访问地址：** http://zbit.info:8888
**定位：** 聚合 AIOps / DevOps / SRE 行业动态、开源工具的每日精选站点

### 核心功能
- 自动抓取 RSS 订阅源（Red Hat、SRE Weekly、InfoQ 等）
- 自动抓取 GitHub Trending（按 AIOps/DevOps/SRE 关键词）
- 固定工具库（精选 10+ 开源工具）
- 每日日报生成
- 每天早 8:00 自动更新

### 技术栈
- **站点生成：** Hugo Extended v0.164.0
- **编程语言：** Python 3.11（抓取脚本）、PowerShell（定时任务）
- **CI/CD：** GitHub Actions
- **服务器：** zbit.info（Ubuntu），nginx 1.28.3
- **版本控制：** Git + GitHub（bugtest/aiops-hot）

---

## 二、项目结构

```
aiops-hot/
├── .github/workflows/deploy.yml   # GitHub Actions 自动部署
├── scripts/
│   ├── config.py                 # 数据源配置（RSS、关键词、工具库）
│   ├── fetch.py                  # 核心抓取脚本（RSS + GitHub）
│   ├── fetch_feeds.py            # RSS 抓取
│   ├── fetch_github.py           # GitHub Trending 抓取
│   ├── run_daily.bat             # Windows 定时任务入口脚本
│   ├── setup_scheduler.ps1        # 定时任务安装脚本
│   └── nginx-aiops-hot.conf      # 服务器 nginx 配置
├── site/                         # Hugo 站点
│   ├── hugo.toml                 # Hugo 配置
│   ├── layouts/                  # HTML 模板
│   ├── static/css/               # 样式
│   └── content/                  # 自动生成的内容
│       ├── articles/             # 行业动态文章
│       ├── tools/                # 工具库
│       └── daily/               # 每日日报
├── data/
│   └── articles_state.json       # 抓取状态（去重记录）
├── README.md                     # 项目说明
└── HANDOVER.md                  # 本文档
```

---

## 三、访问地址

| 环境 | 地址 |
|------|------|
| **线上站点** | http://zbit.info:8888 |
| **GitHub 仓库** | https://github.com/bugtest/aiops-hot |
| **本地预览** | http://localhost:1313（需 `hugo server`） |

> ⚠️ 端口 8888 是因为端口 80 被 Shadowsocks 占用。nginx 监听 8888 和 443。

---

## 四、日常维护

### 4.1 手动触发数据抓取 + 部署

```bash
cd C:\Users\wangc\.qclaw\workspace\aiops-hot

# 1. 抓取数据
python scripts/fetch.py

# 2. 推送到 GitHub（自动触发 CI/CD 部署）
git add -A
git commit -m "update"
git push origin main
```

约 20 秒后，线上站点自动更新。

### 4.2 本地预览（无需推送）

```bash
cd C:\Users\wangc\.qclaw\workspace\aiops-hot/site
hugo server --port 1313
# 访问 http://localhost:1313
```

### 4.3 定时任务状态

计划任务名称：**AIOpsHot_DailyUpdate**
触发时间：**每天早 8:00**
状态查询：
```powershell
SchTasks /Query /TN "AIOpsHot_DailyUpdate" /FO LIST
```

---

## 五、GitHub Actions 部署流程

### 工作流文件
`.github/workflows/deploy.yml`

### 触发条件
每次推送到 `main` 分支

### 执行步骤（约 17 秒）
1. Checkout 代码
2. 安装 Hugo Extended 0.164.0
3. `hugo --source site --quiet` 构建站点
4. SSH 登录 zbit.info
5. `git pull` + `hugo rebuild` 更新站点

### 部署密钥
- Secret 名称：`DEPLOY_KEY`
- 内容：服务器 SSH ED25519 私钥
- 位置：GitHub 仓库 → Settings → Secrets and variables → Actions
- 查看/修改路径：
  ```bash
  gh secret list --repo bugtest/aiops-hot
  gh secret set DEPLOY_KEY --body "$(cat ~/.ssh/id_ed25519)" --repo bugtest/aiops-hot
  ```

### 查看部署状态
```bash
# 最近运行
gh run list --repo bugtest/aiops-hot

# 详细日志
gh run view <run-id> --log --repo bugtest/aiops-hot
```

---

## 六、服务器信息

| 项目 | 值 |
|------|-----|
| 服务器地址 | zbit.info |
| SSH 用户 | ubuntu |
| SSH 私钥 | `C:\Users\wangc\.ssh\id_ed25519` |
| 站点目录 | `/var/www/aiops-hot` |
| Hugo 版本 | v0.164.0 Extended |
| nginx 配置 | `/etc/nginx/sites-available/aiops-hot.conf` |
| nginx 端口 | 8888（80 被 Shadowsocks 占用） |
| HTTPS | 有（443），HTTP 重定向待配置 |

### 服务器日常操作
```bash
# SSH 登录
ssh -i ~/.ssh/id_ed25519 ubuntu@zbit.info

# 手动重建站点
cd /var/www/aiops-hot
git pull origin main
hugo --source site --quiet

# 查看 nginx 错误日志
sudo tail -50 /var/log/nginx/aiops-hot_error.log

# 重载 nginx
sudo systemctl reload nginx

# 验证 nginx 配置
sudo nginx -t
```

---

## 七、添加内容

### 7.1 添加 RSS 订阅源

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

### 7.2 添加固定工具

编辑 `scripts/config.py` 中的 `FEATURED_TOOLS` 列表。

### 7.3 修改 GitHub Trending 关键词

编辑 `scripts/config.py` 中的 `GITHUB_KEYWORDS` 列表。

### 7.4 修改站点标题/描述

编辑 `site/hugo.toml` 中的 `title`、`description`、`params`。

---

## 八、已知的注意点

1. **端口 8888**：服务器端口 80 被 Shadowsocks 占用，nginx 监听 8888。访问时必须带端口号。

2. **SSH 密钥路径**：本地私钥在 `C:\Users\wangc\.ssh\id_ed25519`，无密码。

3. **GitHub Token**：本地 gh CLI 已登录账户 `bugtest`，推送时自动用 token 认证。

4. **Hugo Extended**：抓取脚本依赖 Hugo Extended 版本（带 SCSS 支持），普通版不够用。

5. **articles_state.json**：抓取状态文件用于去重，删除后会导致文章重复出现。

6. **服务器磁盘使用率 94.7%**：系统盘较满，Hugo 构建产物约 20MB，长期运行需关注。

7. **Ubuntu 26.04 LTS**：服务器系统版本较新（24.04基础上），Hugo/nginx 均已就绪。

---

## 九、接下来的优化方向（可选）

- [ ] AI 摘要：为文章自动生成一句话摘要
- [ ] HTTPS 配置：完善 HTTP → HTTPS 强制跳转
- [ ] 更多 RSS 源：覆盖更多大厂技术博客
- [ ] 搜索功能：接入 Pagefind 全文搜索
- [ ] 邮件通知：CI/CD 失败时发送邮件告警
- [ ] 监控：服务器磁盘/内存告警

---

## 十、联系信息

| 用途 | 账户 |
|------|------|
| GitHub 仓库 | bugtest/aiops-hot |
| GitHub CLI 登录 | bugtest |
| 服务器 SSH | ubuntu@zbit.info |
| 站点域名 | zbit.info |

---

**交接完毕。如有问题，请参考 README.md 或查看脚本源码。**

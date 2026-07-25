# -*- coding: utf-8 -*-
import sys, os, io, json, datetime, re, time
from pathlib import Path

# 强制 UTF-8 输出（Windows 兼容）
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# 加载配置
from config import (
    RSS_FEEDS, BLOG_SOURCES, GITHUB_KEYWORDS,
    FEATURED_TOOLS, article_id, today_str,
)

import feedparser
import httpx
from bs4 import BeautifulSoup

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "site" / "content"
STATE_FILE = BASE_DIR / "data" / "articles_state.json"
DATA_DIR.mkdir(parents=True, exist_ok=True)
STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/rss+xml, application/xml, text/html, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
}

http = httpx.Client(headers=HEADERS, timeout=30, follow_redirects=True)

# ========================
# 状态管理（去重）
# ========================
def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return {}

def save_state(state: dict):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# ========================
# 1. RSS 抓取
# ========================
def fetch_rss(feed: dict) -> list:
    items = []
    try:
        print(f"  [RSS] {feed['name']}: ", end="", flush=True)
        resp = http.get(feed["url"])
        resp.raise_for_status()
        feed_data = feedparser.parse(resp.text)

        for entry in feed_data.entries[:15]:
            title = (entry.get("title") or "").strip()
            link = (entry.get("link") or "").strip()
            if not title or not link:
                continue

            summary = ""
            for field in ("summary", "description", "content"):
                if hasattr(entry, field):
                    raw = getattr(entry, field)
                    if raw:
                        soup = BeautifulSoup(raw, "html.parser")
                        summary = soup.get_text(separator=" ", strip=True)
                        break

            published = ""
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                try:
                    dt = datetime.datetime(*entry.published_parsed[:6])
                    published = dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

            aid = article_id(feed["section"], title, link)
            items.append({
                "id": aid,
                "title": title,
                "url": link,
                "source": feed["name"],
                "category": feed["category"],
                "section": feed["section"],
                "tags": feed["tags"],
                "summary": summary[:300],
                "published": published or today_str(),
                "fetched": today_str(),
            })
        print(f"OK {len(items)} 篇")
    except Exception as e:
        print(f"FAIL: {e}")
    return items

# ========================
# 2. 大厂博客页面抓取
# ========================
def fetch_blog_page(source: dict) -> list:
    items = []
    try:
        print(f"  [WEB] {source['name']}: ", end="", flush=True)
        resp = http.get(source["url"])
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        links = []
        keywords = ["运维", "AIOps", "DevOps", "SRE", "监控", "告警",
                    "智能", "K8s", "k8s", "容器", "可观测", "observability",
                    "sre", "oncall", "incident", "prometheus", "grafana"]

        for a in soup.find_all("a", href=True):
            href = a["href"]
            text = a.get_text(strip=True)
            if len(text) > 15 and any(k in text for k in keywords):
                if href.startswith("http") and "javascript" not in href.lower():
                    links.append((text, href))

        seen = {}
        for title, link in links:
            if link not in seen:
                seen[link] = title

        for link, title in list(seen.items())[:10]:
            aid = article_id(source["section"], title, link)
            items.append({
                "id": aid,
                "title": title,
                "url": link,
                "source": source["name"],
                "category": source["category"],
                "section": source["section"],
                "tags": source["tags"],
                "summary": f"来自 {source['name']} 的技术文章",
                "published": today_str(),
                "fetched": today_str(),
            })
        print(f"OK {len(items)} 篇")
    except Exception as e:
        print(f"FAIL: {e}")
    return items

# ========================
# 3. GitHub Trending
# ========================
def fetch_github_trending() -> list:
    items = []
    try:
        print(f"  [GIT] GitHub Trending: ", end="", flush=True)

        for keyword in GITHUB_KEYWORDS[:6]:
            url = (
                f"https://api.github.com/search/repositories"
                f"?q={keyword}+in:name,description,readme"
                f"&sort=stars&order=desc&per_page=5"
            )
            try:
                resp = http.get(url)
                if resp.status_code != 200:
                    continue
                data = resp.json()
                for repo in data.get("items", [])[:3]:
                    rid = article_id("tools", repo["full_name"], repo["html_url"])
                    items.append({
                        "id": rid,
                        "name": repo["full_name"],
                        "title": repo["full_name"].split("/")[1],
                        "desc": repo.get("description") or "",
                        "url": repo["html_url"],
                        "language": repo.get("language") or "-",
                        "stars": f"{repo.get('stargazers_count', 0):,}",
                        "forks": f"{repo.get('forks_count', 0):,}",
                        "issues": f"{repo.get('open_issues_count', 0):,}",
                        "license": (repo.get("license") or {}).get("spdx_id", "-") if repo.get("license") else "-",
                        "tags": [keyword],
                        "fetched": today_str(),
                    })
                time.sleep(0.6)
            except Exception:
                continue

        seen = {}
        for item in items:
            if item["name"] not in seen:
                seen[item["name"]] = item
        items = list(seen.values())[:20]
        print(f"OK {len(items)} 个项目")
    except Exception as e:
        print(f"FAIL: {e}")
    return items

# ========================
# 4. 生成 Hugo 内容文件
# ========================
def slugify(title: str) -> str:
    s = re.sub(r'[^\w\s-]', '', title)
    s = re.sub(r'[-\s]+', '-', s).strip('-')
    return s[:60]

def save_article(item: dict, state: dict) -> bool:
    if item["id"] in state:
        return False
    slug = slugify(item["title"])
    pub = item.get("published", today_str())
    filename = f"{pub}-{slug}.md"
    filepath = DATA_DIR / item["section"] / filename
    if filepath.exists():
        state[item["id"]] = str(filepath)
        return False

    tags_str = ", ".join(f'"{t}"' for t in item.get("tags", []))
    summary_esc = item.get("summary", "")[:200].replace('"', "'")

    content = f'''---
title: "{item['title']}"
date: {pub}T08:00:00+08:00
draft: false
category: "{item['category']}"
source: "{item['source']}"
original_url: "{item['url']}"
tags: [{tags_str}]
summary: "{summary_esc}"
---

{item.get('summary', '')}

[阅读原文]({item['url']})
'''
    filepath.write_text(content, encoding="utf-8")
    state[item["id"]] = str(filepath)
    return True

def save_tool(item: dict, state: dict) -> bool:
    if item["id"] in state:
        return False
    slug = slugify(item.get("name", item.get("title", "tool")))
    filename = f"{slug}.md"
    filepath = DATA_DIR / "tools" / filename
    if filepath.exists():
        state[item["id"]] = str(filepath)
        return False

    tags_str = ", ".join(f'"{t}"' for t in item.get("tags", []))
    desc_esc = item.get("desc", item.get("summary", "")).replace('"', "'")

    content = f'''---
title: "{item.get('name', item.get('title', 'Tool'))}"
date: {today_str()}T08:00:00+08:00
draft: false
category: "tool"
source: "GitHub"
original_url: "{item['url']}"
language: "{item.get('language', '-')}"
stars: "{item.get('stars', '-')}"
forks: "{item.get('forks', '-')}"
issues: "{item.get('issues', '-')}"
license: "{item.get('license', '-')}"
tags: [{tags_str}]
---

## {item.get('name', item.get('title', 'Tool'))}

{desc_esc}

**GitHub**: [{item.get('name', item.get('title'))}]({item['url']})

| 指标 | 值 |
|------|-----|
| Stars | {item.get('stars', '-')} |
| Forks | {item.get('forks', '-')} |
| Issues | {item.get('issues', '-')} |
| Language | {item.get('language', '-')} |
| License | {item.get('license', '-')} |
'''
    filepath.write_text(content, encoding="utf-8")
    state[item["id"]] = str(filepath)
    return True

# ========================
# 5. 每日日报
# ========================
def generate_daily_report(all_articles: list):
    today = datetime.date.today()
    date_str = today.strftime("%Y-%m-%d")
    filename = DATA_DIR / "daily" / f"{date_str}.md"

    categories = {}
    for a in all_articles:
        cat = a.get("category", "other")
        categories[cat] = categories.get(cat, 0) + 1

    top5 = sorted(all_articles, key=lambda x: x.get("weight", 5), reverse=True)[:5]

    cat_map = {"case": "case", "practice": "practice", "news": "news"}
    content = f'''---
title: "{date_str} 日报"
date: {date_str}T08:00:00+08:00
draft: false
category: "daily"
---

# {date_str} 智能运维日报

> 本日报由「智能运维前线」自动聚合生成，涵盖 AIOps / DevOps / SRE 领域今日热点。

## 今日概览

| 分类 | 数量 |
|------|------|
| 大厂案例 | {categories.get('case', 0)} 篇 |
| 技术实践 | {categories.get('practice', 0)} 篇 |
| 行业新闻 | {categories.get('news', 0)} 篇 |

---

## 今日精选

'''
    for i, a in enumerate(top5, 1):
        content += f"{i}. **{a['title']}** - {a['source']}\n\n"

    content += "\n---\n\n## 全部动态\n\n"
    for a in all_articles[:30]:
        content += f"- [{a['title']}]({a['url']}) - {a['source']}\n"

    content += f"""

---
*本日报于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} 自动更新，共收录 {len(all_articles)} 篇*
"""
    filename.write_text(content, encoding="utf-8")
    print(f"  [REP] 日报已生成: {filename.name}")
    return filename

# ========================
# 主流程
# ========================
def main():
    print(f"\n{'='*50}")
    print(f"智能运维前线 - 数据抓取")
    print(f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    state = load_state()
    all_articles = []
    new_count = 0

    # 1. RSS 源
    print("[1/3] 抓取 RSS 源...")
    for feed in RSS_FEEDS:
        items = fetch_rss(feed)
        for item in items:
            if save_article(item, state):
                new_count += 1
            all_articles.append(item)
        time.sleep(0.3)

    # 2. 大厂博客
    print("\n[2/3] 抓取大厂博客...")
    for source in BLOG_SOURCES:
        if source.get("type") == "rss":
            items = fetch_rss(source)
        else:
            items = fetch_blog_page(source)
        for item in items:
            if save_article(item, state):
                new_count += 1
            all_articles.append(item)
        time.sleep(0.5)

    # 3. GitHub Trending
    print("\n[3/3] 抓取 GitHub Trending...")
    trending_tools = fetch_github_trending()
    for tool in trending_tools:
        if save_tool(tool, state):
            new_count += 1

    # 4. 固定工具库
    print("\n[补充] 写入固定工具库...")
    for tool in FEATURED_TOOLS:
        tool["id"] = article_id("tools", tool["name"], tool["url"])
        if save_tool(tool, state):
            new_count += 1

    # 5. 日报
    print("\n[日报] 生成每日日报...")
    generate_daily_report(all_articles)

    save_state(state)

    print(f"\n[DONE] 完成！本次新增 {new_count} 条内容")
    print(f"       累计收录文章 {len(all_articles)} 篇")
    print(f"       状态文件: {STATE_FILE}")

if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
智能运维前线 — 数据配置
定义所有 RSS 源和大厂博客来源
"""
import hashlib, datetime

# ========================
# RSS 源配置（行业动态）
# 精选全球技术含量最高的 AIOps / DevOps / SRE / 可观测性博客
# ========================
RSS_FEEDS = [
    # ── 中文优质源（保留） ──
    {
        "name": "InfoQ中国",
        "url": "https://news.cn.infoq.com/rss/",
        "category": "practice",
        "section": "articles",
        "tags": ["实践", "架构", "中国"],
        "weight": 9,
    },
    {
        "name": "腾讯云+开发者",
        "url": "https://cloud.tencent.com/developer/rss/list/255",
        "category": "practice",
        "section": "articles",
        "tags": ["腾讯云", "实践", "中国"],
        "weight": 8,
    },

    # ── SRE 行业资讯 ──
    {
        "name": "SRE Weekly",
        "url": "https://sreweekly.com/feed",
        "category": "practice",
        "section": "articles",
        "tags": ["SRE", "运维", "国际"],
        "weight": 7,
    },

    # ── 一线工程团队博客（技术深度最高） ──
    {
        "name": "Google Cloud SRE",
        "url": "https://cloud.google.com/blog/products/devops-sre/rss",
        "category": "practice",
        "section": "articles",
        "tags": ["Google", "SRE", "国际", "可观测性"],
        "weight": 10,
        "note": "Google SRE 团队官方博客，《SRE 白皮书》原班人马，Agentic AI 运维前沿",
    },
    {
        "name": "Netflix Tech Blog",
        "url": "https://netflixtechblog.com/feed",
        "category": "practice",
        "section": "articles",
        "tags": ["Netflix", "分布式系统", "国际", "SRE"],
        "weight": 10,
        "note": "混沌工程发源地，大规模分布式系统实战经验，每篇都是硬核技术文",
    },
    {
        "name": "The New Stack",
        "url": "https://thenewstack.io/feed/",
        "category": "practice",
        "section": "articles",
        "tags": ["云原生", "DevOps", "国际", "AI"],
        "weight": 10,
        "note": "独立科技媒体，云原生/可观测性/AIOps 全覆盖，技术深度行业领先",
    },

    # ── 可观测性生态核心博客 ──
    {
        "name": "Honeycomb Blog",
        "url": "https://www.honeycomb.io/blog/feed.xml",
        "category": "practice",
        "section": "articles",
        "tags": ["Observability", "可观测性", "国际", "eBPF"],
        "weight": 9,
        "note": "可观测性 2.0 概念推动者，CTO Charity Majors 亲笔，高基数数据深度技术",
    },
    {
        "name": "Grafana Labs Blog",
        "url": "https://grafana.com/blog/index.xml",
        "category": "practice",
        "section": "articles",
        "tags": ["Grafana", "Prometheus", "可观测性", "国际"],
        "weight": 9,
        "note": "开源可观测性生态核心，Prometheus/Loki/Tempo/Mimir 全栈最佳实践",
    },
    {
        "name": "Elastic Observability",
        "url": "https://elastic-dev.co/observability-labs/feed/",
        "category": "practice",
        "section": "articles",
        "tags": ["Elastic", "AIOps", "日志", "国际"],
        "weight": 8,
        "note": "ELK 栈 AIOps 日志智能分析，ML 驱动异常检测实战文章",
    },

    # ── 事件管理 & AI SRE ──
    {
        "name": "incident.io Blog",
        "url": "https://incident.io/blog/feed.xml",
        "category": "practice",
        "section": "articles",
        "tags": ["SRE", "事件管理", "AI", "国际"],
        "weight": 8,
        "note": "AI SRE 实践先驱，覆盖事件管理、告警治理、On-call 最佳实践",
    },
    {
        "name": "Datadog Engineering",
        "url": "https://www.datadoghq.com/blog/feed/",
        "category": "practice",
        "section": "articles",
        "tags": ["Datadog", "APM", "监控", "国际"],
        "weight": 8,
        "note": "全球最大 APM 平台工程博客，分布式追踪/基础设施监控深度技术",
    },
    {
        "name": "PagerDuty Blog",
        "url": "https://www.pagerduty.com/blog/feed/",
        "category": "practice",
        "section": "articles",
        "tags": ["事件响应", "AIOps", "自动化", "国际"],
        "weight": 7,
        "note": "事件管理标杆企业，AIOps 实践与数字化运维案例",
    },
]

# ========================
# 大厂博客列表（直接 HTTP 抓取）
# ========================
BLOG_SOURCES = [
    {
        "name": "腾讯云AIOps实践",
        "url": "https://cloud.tencent.com/developer/column/1313",
        "search_url": "https://cloud.tencent.com/developer/api/column/getColumnArticleList",
        "category": "case",
        "section": "articles",
        "tags": ["腾讯云", "AIOps", "案例"],
        "weight": 10,
        "type": "ajax_json",
    },
    {
        "name": "AWS DevOps & SRE",
        "url": "https://aws.amazon.com/blogs/devops/",
        "category": "case",
        "section": "articles",
        "tags": ["AWS", "DevOps", "案例"],
        "weight": 9,
        "type": "rss",
    },
]

# ========================
# GitHub Trending 关键词过滤
# ========================
GITHUB_KEYWORDS = [
    "aiops", "sre", "devops", "observability", "prometheus", "grafana",
    "opentracing", "opentelemetry", "jaeger", "skywalking", "sentry",
    "kubernetes", "k8s", "monitoring", "alertmanager", "pagerduty",
    "ansible", "terraform", "vault", "argocd", "flux", "jenkins",
    "cicd", "elasticsearch", "logstash", "kibana", "fluentd",
    "zabbix", "nagios", "datadog", "newrelic", "dynatrace",
    "keep", "opsgenie", "runbook", "incident", "oncall",
    # 新增：AIOps / 可观测性前沿
    "ebpf", "openobserve", "signoz", "pixie", "chaos-mesh",
    "litmus", "crossplane", "kyverno", "kube-prometheus",
    "opentelemetry-operator", "vector", "alloy",
    "langchain", "llm-ops", "agentic-ops",
]

# GitHub Trending API（无需 token）
GITHUB_TRENDING_URL = "https://api.github.com/search/repositories"

# ========================
# 工具/开源项目数据（固定+Trending 补充）
# ========================
FEATURED_TOOLS = [
    {
        "name": "Keep",
        "full_name": "kai-nerd/keep",
        "desc": "开源 AIOps 告警管理平台，支持多数据源告警聚合、根因分析、自动修复工作流",
        "language": "Python",
        "stars": "10.2k",
        "forks": "1.1k",
        "issues": "500+",
        "license": "MIT",
        "url": "https://github.com/kai-nerd/keep",
        "tags": ["AIOps", "告警", "SRE"],
    },
    {
        "name": "AIOPS Tools",
        "full_name": "jixinpu/aiopstools",
        "desc": "Python AIOps 工具库，支持日志分析、异常检测、性能监控、自动修复",
        "language": "Python",
        "stars": "3.8k",
        "forks": "820",
        "issues": "120+",
        "license": "MIT",
        "url": "https://github.com/jixinpu/aiopstools",
        "tags": ["AIOps", "Python", "异常检测"],
    },
    {
        "name": "Grype",
        "full_name": "anchore/grype",
        "desc": "容器镜像漏洞扫描工具，Go 编写，速度极快，支持 OCI 和 Docker 镜像",
        "language": "Go",
        "stars": "8.7k",
        "forks": "680",
        "issues": "200+",
        "license": "Apache-2.0",
        "url": "https://github.com/anchore/grype",
        "tags": ["安全", "容器", "DevOps"],
    },
    {
        "name": "Trivy",
        "full_name": "aquasecurity/trivy",
        "desc": "容器和 Kubernetes 安全扫描工具，支持漏洞、秘钥、许可证扫描",
        "language": "Go",
        "stars": "22.4k",
        "forks": "2.1k",
        "issues": "900+",
        "license": "Apache-2.0",
        "url": "https://github.com/aquasecurity/trivy",
        "tags": ["安全", "K8s", "DevOps"],
    },
    {
        "name": "OpenTelemetry Collector",
        "full_name": "open-telemetry/opentelemetry-collector",
        "desc": "可观测性数据收集器，统一处理 traces、metrics、logs",
        "language": "Go",
        "stars": "5.2k",
        "forks": "1.3k",
        "issues": "600+",
        "license": "Apache-2.0",
        "url": "https://github.com/open-telemetry/opentelemetry-collector",
        "tags": ["可观测性", "Otel", "监控"],
    },
    {
        "name": "Weave GitOps",
        "full_name": "weaveworks/weave-gitops",
        "desc": "GitOps 运维平台，基于 Flux，提供 Web UI 和自动化部署",
        "language": "Go",
        "stars": "4.1k",
        "forks": "580",
        "issues": "300+",
        "license": "Apache-2.0",
        "url": "https://github.com/weaveworks/weave-gitops",
        "tags": ["GitOps", "K8s", "CI/CD"],
    },
    {
        "name": "VictoriaMetrics",
        "full_name": "VictoriaMetrics/VictoriaMetrics",
        "desc": "高性能时序数据库，Prometheus 兼容，适合大规模监控数据存储",
        "language": "Go",
        "stars": "16.8k",
        "forks": "1.4k",
        "issues": "700+",
        "license": "Apache-2.0",
        "url": "https://github.com/VictoriaMetrics/VictoriaMetrics",
        "tags": ["时序库", "监控", "Prometheus"],
    },
    {
        "name": "Keep (Alert Management)",
        "full_name": "opsgenie/keep",
        "desc": "OpsGenie 开源版告警管理平台，统一管理 PagerDuty、DataDog 等告警",
        "language": "Python",
        "stars": "9.8k",
        "forks": "1.0k",
        "issues": "450+",
        "license": "MIT",
        "url": "https://github.com/opsgenie/keep",
        "tags": ["AIOps", "告警", "SRE"],
    },
    {
        "name": "Thanos",
        "full_name": "thanos-io/thanos",
        "desc": "Prometheus 长时存储与全局视图，支持跨集群查询和高可用",
        "language": "Go",
        "stars": "13.2k",
        "forks": "1.8k",
        "issues": "800+",
        "license": "Apache-2.0",
        "url": "https://github.com/thanos-io/thanos",
        "tags": ["监控", "Prometheus", "K8s"],
    },
    {
        "name": "Pixie",
        "full_name": "pixie-io/pixie",
        "desc": "Kubernetes 无侵入可观测性平台，基于 eBPF，自动采集应用性能数据",
        "language": "Go",
        "stars": "7.4k",
        "forks": "620",
        "issues": "350+",
        "license": "Apache-2.0",
        "url": "https://github.com/pixie-io/pixie",
        "tags": ["K8s", "eBPF", "可观测性"],
    },
]

# ========================
# 工具函数
# ========================
def make_hash(title: str, url: str) -> str:
    """生成文章唯一 ID"""
    raw = f"{title}|{url}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()[:12]

def today_str() -> str:
    return datetime.date.today().strftime("%Y-%m-%d")

def article_id(prefix: str, title: str, url: str) -> str:
    h = make_hash(title, url)
    return f"{prefix}-{h}"

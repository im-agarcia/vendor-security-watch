"""Copia este archivo a config.py y editalo con tus propios datos.
config.py se commitea normalmente al repo (no tiene secretos: el webhook URL
real vive aparte, como GitHub Actions Secret NOTIFIER_WEBHOOK_URL).
"""

# "slack" o "teams". Para sumar otro sistema, ver scripts/notifiers/base.py.
NOTIFIER = "slack"

# Palabras clave reutilizables para filtrar ruido (case-insensitive, matchea
# contra el titulo del item). Ver docs/sources.md.
#
# Ejemplo: si solo usas AWS/GCP para un load balancer, no te interesa el
# catalogo entero del vendor, solo bulletins de networking/IAM.
NETWORKING_IAM_KEYWORDS = [
    "load balanc", "elb", "alb", "nlb", "vpc", "iam", "network", "security group",
    "firewall", "route 53", "route53", "waf", "gateway", "nat ", "cloud armor", "dns",
]

# Vendors SaaS puro no tienen advisory feed propio (ellos parchean, no vos),
# pero igual conviene saber si tuvieron un incidente de seguridad para tu
# plan de respuesta a incidentes. Filtra su status page a palabras clave de
# seguridad para no traer downtime comun.
SAAS_SECURITY_KEYWORDS = [
    "security", "vulnerab", "unauthorized", "breach", "compromise", "credential",
    "exploit", "token leak", "leaked", "incident response", "data expos",
]

# Tus fuentes. Cada entrada es una de estas 3 formas:
#
# CVE feed de un proyecto open source (via GitHub Security Advisories API):
#   {"name": "...", "type": "github_advisories", "repo": "org/repo"}
#
# Bulletin RSS/Atom de un proveedor cloud (opcionalmente filtrado):
#   {"name": "...", "type": "rss"|"atom", "url": "...", "keywords": [...]}
#
# Status page de un SaaS, filtrada a incidentes de seguridad:
#   {"name": "...", "type": "atom", "url": "https://status.<vendor>.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS}
#
# Los que siguen son ejemplos reales y funcionales (feeds verificados), pensados
# para un stack tipico de infra + SaaS. Borra los que no uses y sumá los tuyos.
SOURCES = [
    # --- CVE feeds ---
    {"name": "AWS", "type": "rss", "url": "https://aws.amazon.com/security/security-bulletins/rss/feed/", "keywords": NETWORKING_IAM_KEYWORDS},
    {"name": "GCP - Compute Engine", "type": "atom", "url": "https://cloud.google.com/feeds/compute-security-bulletins.xml", "keywords": NETWORKING_IAM_KEYWORDS},
    {"name": "GCP - GKE", "type": "atom", "url": "https://cloud.google.com/feeds/gke-security-bulletins.xml", "keywords": NETWORKING_IAM_KEYWORDS},
    {"name": "New Relic", "type": "rss", "url": "https://docs.newrelic.com/docs/security/new-relic-security/security-bulletins/feed.xml"},
    {"name": "Sentry", "type": "github_advisories", "repo": "getsentry/sentry"},
    {"name": "PostHog", "type": "github_advisories", "repo": "PostHog/posthog"},
    {"name": "Grafana", "type": "github_advisories", "repo": "grafana/grafana"},
    # Advisories oficiales de Grafana Labs: cubren mas que el repo core (plugins, MCP server, Enterprise).
    {"name": "Grafana Labs (grafana.com)", "type": "rss", "url": "https://grafana.com/security/security-advisories/index.xml"},
    {"name": "Metabase", "type": "github_advisories", "repo": "metabase/metabase"},
    {"name": "Open WebUI", "type": "github_advisories", "repo": "open-webui/open-webui"},
    {"name": "GrowthBook", "type": "github_advisories", "repo": "growthbook/growthbook"},
    # --- Status pages filtradas a seguridad (SaaS sin CVE feed propio) ---
    {"name": "GitHub", "type": "atom", "url": "https://www.githubstatus.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "Anthropic", "type": "atom", "url": "https://status.anthropic.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "Atlassian (Jira/Bitbucket)", "type": "atom", "url": "https://status.atlassian.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "Google Workspace", "type": "atom", "url": "https://www.google.com/appsstatus/dashboard/en/feed.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "MongoDB Atlas", "type": "atom", "url": "https://status.mongodb.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "Notion", "type": "atom", "url": "https://www.notion-status.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "Twilio", "type": "atom", "url": "https://status.twilio.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "1Password (AgileBits)", "type": "atom", "url": "https://1password.statuspage.io/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
]

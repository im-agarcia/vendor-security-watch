"""Copia este archivo a config.py y editalo con tus propios datos.
config.py se commitea normalmente al repo (no tiene secretos: el webhook URL
real vive aparte, como GitHub Actions Secret NOTIFIER_WEBHOOK_URL).
"""

# "slack" o "teams". Para sumar otro sistema, ver scripts/notifiers/base.py.
NOTIFIER = "slack"

# Palabras clave reutilizables para filtrar ruido (case-insensitive, matchea
# contra el titulo del item). Ver docs/sources.md.
NETWORKING_IAM_KEYWORDS = [
    "load balanc", "elb", "alb", "nlb", "vpc", "iam", "network",
    "security group", "firewall", "waf", "gateway",
]
SAAS_SECURITY_KEYWORDS = [
    "security", "vulnerab", "unauthorized", "breach", "compromise",
    "credential", "exploit", "leaked", "data expos",
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
SOURCES = [
    {"name": "AWS", "type": "rss", "url": "https://aws.amazon.com/security/security-bulletins/rss/feed/", "keywords": NETWORKING_IAM_KEYWORDS},
    {"name": "GitHub", "type": "atom", "url": "https://www.githubstatus.com/history.atom", "keywords": SAAS_SECURITY_KEYWORDS},
    {"name": "MiHerramientaOpenSource", "type": "github_advisories", "repo": "org/repo"},
]

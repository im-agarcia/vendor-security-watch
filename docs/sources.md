# Cómo elegir tus fuentes

Hay tres tipos de proveedores, y cada uno necesita una fuente distinta. Todas se configuran en `config.py`, en la lista `SOURCES`.

## A) Herramientas open source (self-hosted o que podrían estarlo)

Publican CVEs formales con versión afectada/parcheada, vía **GitHub Security Advisories**:

```python
{"name": "Metabase", "type": "github_advisories", "repo": "metabase/metabase"}
```

Fuente: `GET https://api.github.com/repos/{owner}/{repo}/security-advisories` — pública, sin autenticación (rate limit más generoso si el workflow usa `GITHUB_TOKEN`, ya incluido).

## B) Proveedores cloud (AWS, GCP, etc.)

Publican bulletins de seguridad propios con feed RSS/Atom dedicado:

```python
{"name": "AWS", "type": "rss", "url": "https://aws.amazon.com/security/security-bulletins/rss/feed/"}
```

Si solo usás una parte acotada del proveedor (ej. únicamente un load balancer en AWS), agregá `"keywords"` para filtrar ruido de servicios que no usás — solo se notifica si el título matchea alguna palabra:

```python
{"name": "AWS", "type": "rss", "url": "...", "keywords": NETWORKING_IAM_KEYWORDS}
```

## C) SaaS puro (Slack, Notion, tu CRM, etc.)

No publican CVEs — el proveedor parchea de su lado. Pero igual importa saber si tuvieron un **incidente de seguridad/brecha**, para tu plan de respuesta a incidentes (evaluar impacto, notificar clientes si corresponde).

La fuente más confiable y gratuita acá es su **status page pública** (la mayoría corre sobre Atlassian Statuspage y expone `/history.atom`), filtrada por palabras clave de seguridad para no traer downtime común:

```python
{"name": "Slack", "type": "atom", "url": "https://slack-status.com/feed/rss", "keywords": SAAS_SECURITY_KEYWORDS}
```

Priorizá esto por nivel de riesgo/criticidad del proveedor — si tenés un inventario de vendors (Vanta, Drata, o incluso una planilla), usalo para ordenar qué vale la pena cubrir primero. No hace falta cubrir el 100% de tus proveedores desde el día uno.

## Trade-off del filtro por keywords

Si el proveedor no usa esas palabras en el título del incidente, se puede escapar. Esto no reemplaza la notificación formal que el proveedor debería enviar ante una brecha real — es una capa adicional de detección temprana, no la única.

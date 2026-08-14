# Vendor Security Watch

Monitoreo automático y gratuito de advisories de seguridad (CVEs) e incidentes de tus proveedores (cloud, SaaS, herramientas internas), con alertas directo a Slack/Teams/lo que uses. Corre en GitHub Actions, sin infraestructura propia ni costo.

```
┌─────────────────┐   cada N horas   ┌───────────────────────┐   item nuevo   ┌──────────┐
│  GitHub Actions  │ ───────────────▶ │ Fuentes oficiales       │ ─────────────▶ │ Slack /  │
│    (cron job)    │                  │ (CVE feeds / status page │                │ Teams /  │
└─────────────────┘                  │  de tus vendors)         │                │ lo tuyo  │
                                      └───────────────────────┘                └──────────┘
```

## Quick start

1. **Usá este repo como template** (botón "Use this template" en GitHub) o cloná y quitá el historial.
2. Copiá `config.example.py` a `config.py` y editalo con tus propios vendors — ver [docs/sources.md](docs/sources.md). `config.example.py` ya trae **19 fuentes reales y verificadas** como ejemplo (AWS, GCP, GitHub, New Relic, Sentry, PostHog, Grafana, Metabase, Open WebUI, GrowthBook, Anthropic, Atlassian, Google Workspace, MongoDB Atlas, Notion, Twilio, 1Password) — borrá las que no uses y sumá las tuyas.
3. Elegí tu sistema de mensajería y seguí los pasos — ver [docs/notifiers.md](docs/notifiers.md).
4. Guardá la URL del webhook como secret `NOTIFIER_WEBHOOK_URL` en **Settings → Secrets and variables → Actions**.
5. Corré el workflow manualmente una vez (**Actions → Vendor security watch → Run workflow**) para bootstrapear el estado inicial, sin recibir mensajes retroactivos.

Listo — a partir de ahí corre solo según el cron que dejaste en `.github/workflows/vendor-security-watch.yml`.

## Estructura

```
config.example.py              # copiar a config.py y editar (tus vendors + notifier)
scripts/
  watch.py                     # pipeline generico, no se toca
  notifiers/
    slack.py
    teams.py
    __init__.py                # registro de notifiers disponibles
.github/workflows/
  vendor-security-watch.yml    # corre el pipeline segun cron
  vendor-list-review.yml       # abre un issue mensual para revisar config.py
docs/
  sources.md                   # como elegir/agregar fuentes
  notifiers.md                 # como configurar Slack/Teams/otro
  maintenance.md               # la rama `state`, revision periodica, costo
```

## Por qué existe esto

Los equipos de seguridad suelen enterarse tarde de que un proveedor publicó una vulnerabilidad crítica, o de que tuvo una brecha — normalmente por casualidad. Esto automatiza el chequeo de las fuentes oficiales varias veces al día y avisa apenas hay algo nuevo, para poder parchear a tiempo o activar el plan de respuesta a incidentes si corresponde.

## Seguridad de este setup

- Solo hace lecturas (`GET`) a endpoints públicos — no hay credenciales propias en el fetch de datos.
- El único secreto (`NOTIFIER_WEBHOOK_URL`) va cifrado en GitHub Secrets, nunca en el código ni en logs.
- El contenido de los feeds se trata siempre como texto a mostrar, nunca se ejecuta.
- Blast radius si el webhook se filtrara: alguien podría postear texto en ese canal. Nada más.

## ¿Preferís que Claude te lo configure?

Ver [PROMPT.md](PROMPT.md) — un prompt listo para pegarle a Claude (Code o claude.ai) junto con este repo, para que te haga las preguntas necesarias y te deje todo andando.

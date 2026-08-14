# Configurar tu sistema de mensajería

Elegís el notifier en `config.py` (`NOTIFIER = "slack"` o `"teams"`) y guardás la URL del webhook como el secret `NOTIFIER_WEBHOOK_URL` en tu repo. El pipeline (`scripts/watch.py`) no sabe ni le importa a qué sistema le está hablando — eso vive enteramente en `scripts/notifiers/`.

## Slack

1. [api.slack.com/apps](https://api.slack.com/apps) → **Create New App** → **Blank app**.
2. Nombre + workspace.
3. Menú lateral → **Incoming Webhooks** → activar el toggle.
4. **Add New Webhook to Workspace** (puede requerir aprobación de un admin del workspace).
5. Elegí el canal → **Allow**.
6. Copiá la **Webhook URL** (`https://hooks.slack.com/services/...`).

## Teams

Microsoft retiró los Incoming Webhook connectors clásicos: hoy el equivalente es un **flujo de Power Automate**.

1. En el canal de Teams → **...** → **Workflows**.
2. Buscá la plantilla **"Post to a channel when a webhook request is received"**.
3. Al crearlo, te da una URL de trigger — esa es tu webhook.
4. En el diseñador del flujo, mapeá el campo `text` del JSON entrante (ver `scripts/notifiers/teams.py`) al cuerpo del mensaje que postea en el canal.

El payload que manda este repo a Teams tiene esta forma:

```json
{"source": "AWS", "title": "...", "link": "...", "text": "🚨 AWS — ..."}
```

## Guardar el secret

En tu repo: **Settings → Secrets and variables → Actions → New repository secret**
- Nombre: `NOTIFIER_WEBHOOK_URL`
- Valor: la URL del webhook

Esa URL funciona como un token: quien la tenga puede postear texto en ese canal/flujo específico, nada más (no lee mensajes ni accede a otra info del workspace). Por eso nunca va en el código, solo como secret.

## Sumar otro sistema (Discord, email, PagerDuty, etc.)

1. Creá `scripts/notifiers/<nombre>.py` con una función `notify(source_name, item)` — mirá `slack.py` o `teams.py` como referencia.
2. Registrala en `scripts/notifiers/__init__.py`.
3. Poné `NOTIFIER = "<nombre>"` en tu `config.py`.

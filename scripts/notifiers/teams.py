import os

import requests

WEBHOOK_URL = os.environ.get("NOTIFIER_WEBHOOK_URL")


def notify(source_name, item):
    """Posta a un flujo de Power Automate ("Post to a channel when a webhook
    request is received"), que es como Teams maneja webhooks entrantes desde
    que retiraron los Incoming Webhook connectors clasicos. Ver docs/notifiers.md
    para como mapear estos campos al mensaje en el flujo.
    """
    if not WEBHOOK_URL:
        print(f"[warn] NOTIFIER_WEBHOOK_URL no configurado: {source_name} - {item['title']}")
        return
    payload = {
        "source": source_name,
        "title": item["title"],
        "link": item["link"],
        "text": f"🚨 {source_name} — {item['title']}",
    }
    resp = requests.post(WEBHOOK_URL, json=payload, timeout=15)
    resp.raise_for_status()

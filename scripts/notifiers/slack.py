import os

import requests

WEBHOOK_URL = os.environ.get("NOTIFIER_WEBHOOK_URL")


def notify(source_name, item):
    if not WEBHOOK_URL:
        print(f"[warn] NOTIFIER_WEBHOOK_URL no configurado: {source_name} - {item['title']}")
        return
    text = f":rotating_light: *{source_name}* — {item['title']}\n{item['link']}"
    resp = requests.post(WEBHOOK_URL, json={"text": text}, timeout=15)
    resp.raise_for_status()

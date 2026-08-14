"""Interfaz que debe cumplir cualquier notifier.

Un notifier es simplemente una funcion:

    def notify(source_name: str, item: dict) -> None

donde `item` tiene las keys: id, title, link.

Para agregar un sistema de mensajeria nuevo (Discord, email, PagerDuty, etc.):
1. Crear scripts/notifiers/<nombre>.py con una funcion `notify(source_name, item)`.
2. Registrarla en scripts/notifiers/__init__.py.
3. Poner NOTIFIER = "<nombre>" en config.py.
"""

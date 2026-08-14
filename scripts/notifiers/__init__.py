from . import slack, teams

_REGISTRY = {
    "slack": slack.notify,
    "teams": teams.notify,
}


def get_notifier(name):
    try:
        return _REGISTRY[name]
    except KeyError:
        raise ValueError(f"Notifier desconocido: {name!r}. Opciones: {list(_REGISTRY)}")

# Mantenimiento

## La rama `state`

El estado (qué IDs ya se notificaron, en `state/seen.json`) vive en una rama **`state`** separada, no en `main`. Dos razones:

1. Si `main` tiene protección de rama ("solo cambios vía PR"), un bot no puede commitear ahí — y no queremos debilitar esa regla solo para que el bot pueda escribir un JSON.
2. El workflow hace `git checkout -B state` seguido de `git push --force`: como esa rama arranca siempre del HEAD actual de `main` (que va cambiando), cada corrida parte de una base distinta a la del `state` remoto anterior. Un push normal fallaría por non-fast-forward. Como esta rama no tiene historia que preservar (es solo un JSON mutable), el force push es seguro acá.

## Revisión periódica de la lista de vendors

Los proveedores cambian con el tiempo — herramientas nuevas, otras que se dan de baja. El workflow `vendor-list-review.yml` abre automáticamente un issue el día 1 de cada mes recordando revisar `config.py`. Ajustá el cron si preferís otra frecuencia.

## Primera corrida

La primera vez que corre el pipeline sobre una fuente nueva, solo guarda el estado inicial — **no manda mensajes retroactivos** de todo el historial que ya existía. Recién a partir de la segunda corrida notifica lo nuevo. Esto aplica por fuente: si agregás una fuente nueva más adelante, esa fuente puntual vuelve a bootstrapear en silencio la primera vez.

## Costo

Todo corre en el free tier de GitHub Actions. Si tu org ya consume mucho de ese free tier con otros workflows, bajá la frecuencia del cron (`vendor-security-watch.yml`) a una corrida diaria en vez de dos.

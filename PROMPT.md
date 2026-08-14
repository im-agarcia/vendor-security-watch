# Prompt para Claude

Pegá esto en una conversación con Claude (Claude Code, recomendado, porque va a necesitar crear un repo y correr comandos) junto con acceso a este template repo (cloná/copiá esta carpeta al working directory, o pasale la URL del template).

---

Quiero que me armes un sistema de "Vendor Security Watch": un monitoreo automático y gratuito que me avise quiero de una vulnerabilidad de seguridad publicada por alguno de mis proveedores.

Estoy usando como base el template de este repo (carpeta actual / [URL del template]). Contiene:
- `scripts/watch.py`: el pipeline, no lo edites salvo que yo pida un cambio de lógica.
- `scripts/notifiers/`: Slack y Teams ya implementados como notifiers plugables.
- `config.example.py`: lo tenés que copiar a `config.py` y completar conmigo.
- `docs/sources.md`, `docs/notifiers.md`, `docs/maintenance.md`: leelos antes de arrancar, tienen el razonamiento detrás de cada decisión de diseño.

Hacé esto en orden:

1. **Preguntame qué proveedores quiero monitorear.** Si tengo un inventario de vendors (Vanta, Drata, una planilla, lo que sea), pedime que te lo pase y usalo para priorizar por nivel de riesgo — no hace falta cubrir el 100% desde el dia uno.

2. **Clasificá cada proveedor** según `docs/sources.md`: ¿es open source (self-hosted o que podría estarlo)? ¿es un proveedor cloud con bulletins propios? ¿es SaaS puro sin CVEs formales? Para los SaaS puros, buscá su status page pública (`/history.atom` es el patrón más común, corren sobre Atlassian Statuspage) — necesito saber cuándo tienen un incidente de seguridad para mi plan de respuesta a incidentes, aunque ellos lo parcheen solo.

3. **Antes de poner cualquier URL de feed en `config.py`, verificala con una llamada real** (`curl`/fetch), no la inventes ni asumas que existe por convención de nombres. Si un feed no existe o redirige a HTML en vez de XML, decímelo y buscamos la alternativa correcta juntos.

4. **Si solo uso una parte acotada de un proveedor cloud** (ej. un load balancer nomás en AWS), armá un filtro de keywords para no traer ruido de servicios que no uso — no lo asumas, preguntame cuál es mi superficie real de uso antes de elegir las palabras clave.

5. **Preguntame qué sistema de mensajería quiero** (Slack, Teams, u otro) y guiame paso a paso para crear el webhook — sin pedirme que te pegue la URL del webhook en el chat. Decime el nombre del secret que tengo que cargar (`NOTIFIER_WEBHOOK_URL`) y dónde.

6. **Creá el repo** (o usá uno existente si te digo cuál) con la estructura de este template. Si el repo tiene protección de rama en `main` ("solo cambios vía PR"), no la debilites: usá el patrón de rama `state` separada que ya viene en `.github/workflows/vendor-security-watch.yml` para el estado mutable.

7. **Probá el pipeline de punta a punta antes de darlo por terminado**: disparalo manualmente (`workflow_dispatch`), revisá los logs, confirmá que el primer run bootstrapea sin mandar mensajes retroactivos. Si querés validar que el envío al canal funciona de verdad (no solo que el código corre), podés "olvidar" un ID ya visto en `state/seen.json` para forzar una notificación de prueba — avisame que es una prueba antes de mostrarme el resultado, no lo dejes ambiguo.

8. **Dejá andando el workflow de revisión mensual** (`vendor-list-review.yml`) y probalo también con `workflow_dispatch` para confirmar que efectivamente abre el issue.

9. **Al final, resumime**: qué fuentes quedaron activas, con qué frecuencia corre, dónde vive el estado, y qué pasos manuales me faltan a mí (aprobar el webhook, etc.).

No asumas nada que puedas verificar con una herramienta. Si algo requiere una decisión mía (nombre del repo, org, frecuencia del cron, qué proveedores priorizar), preguntame en vez de elegir por tu cuenta.

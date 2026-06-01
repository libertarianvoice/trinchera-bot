# Trinchera Libertaria Bot

**Bot oficial de Telegram para la Trinchera de Libertarian Voice** (@lv_trinchera_bot)

100% libertario. Estilo Milei. Anti-zurdos. Humor negro.  
**"Viva la libertad, carajo."**

---

## Características (Versión Ligera - Sin Base de Datos)

- ✅ **Bienvenida automática EXACTA** (texto oficial de Libertarian Voice)
- ✅ **Moderación SOLO spam/flood/trolls** — Nunca toca admins ni opiniones políticas (aunque sean zurdas)
- ✅ **`/pregunta`** — Responde con Grok (xAI) en estilo Milei / Libertarian Voice puro
- ✅ **`/sticker`** — Genera stickers con Grok Imagine (límite diario en memoria)
- ✅ **`/crear_encuesta`** — Crea polls nativos de Telegram (solo admins)
- ✅ **`/stats`** — Estadísticas de la sesión actual (uptime, contadores en memoria) — solo admins
- ✅ **`/start` + `/ayuda`** básicos
- ⚡ **Zero DB**: Sin PostgreSQL, Alembic, SQLAlchemy ni asyncpg. Todo en memoria + .env
- 🪶 Muy ligero y fácil de correr localmente

---

## Stack Técnico (Versión Minimalista)

- Python 3.11+
- aiogram 3.20+ 
- xai-sdk (Grok chat + Imagine)
- Pillow + httpx (stickers)
- Pydantic Settings v2
- **Sin base de datos** (intencional)

---

## Inicio Rápido (Ahora es trivial - sin DB)

### Requisitos
- Python 3.11+
- uv (recomendado) o pip

### Pasos (Windows PowerShell)

```powershell
# 1. Instalar uv si no tenés (una sola vez)
irm https://astral.sh/uv/install.ps1 | iex

cd trinchera-bot

# 2. Instalar dependencias (sin postgres ni nada)
uv sync

# 3. Copiar y editar .env (usá el que ya tenés)
cp .env.example .env
# Editá .env con BOT_TOKEN, XAI_API_KEY, TRINCHERA_CHAT_ID y ADMIN_USER_IDS

# 4. Correr el bot (ver instrucciones exactas al final de este README)
```

**No hace falta Docker, Postgres, migraciones ni Alembic.**

---

## Configuración Obligatoria en @BotFather

1. Crear bot → `@lv_trinchera_bot`
2. `/setprivacy` → **Disable**
3. `/setjoingroups` → **Enable**
4. `/setcommands` — pegar (versión ligera):

```
start - Información de la Trinchera
pregunta - Preguntale algo al Grok libertario
sticker - Genera un sticker libertario
crear_encuesta - Crear encuesta (solo admins)
stats - Estadísticas del bot (solo admins)
ayuda - Lista de comandos
```

5. Agregar el bot al grupo **Trinchera** como **Administrador** con permisos:
   - Eliminar mensajes
   - Banear usuarios
   - Fijar mensajes

---

## Variables de Entorno (.env)

Ver archivo `.env.example` (está comentado y completo).

**Obligatorias (sin DB):**
- `BOT_TOKEN`
- `XAI_API_KEY` (https://console.x.ai)
- `TRINCHERA_CHAT_ID` (negativo)
- `ADMIN_USER_IDS` (separados por coma)

**Recomendada:**
- `LOG_CHANNEL_ID` (logs de moderación)

---

## Deploy (Ahora mucho más simple)

- **Sin Postgres** → podés deployar en cualquier PaaS gratis (Railway, Render, Fly, VPS barato).
- El `Dockerfile` original todavía funciona (quitale las partes de alembic/migrations si querés).
- Variables: solo las 4-5 obligatorias.
- Para alta escala futura podés agregar Redis para rate limits y stats persistentes.

---

## Estructura Actual (Minimalista)

```
src/trinchera_bot/
├── main.py
├── bot.py
├── application.py
├── config.py
├── constants.py
├── utils/
│   └── stats.py          # Contadores en memoria
├── handlers/
│   ├── chat_member.py    # Bienvenida EXACTA (sin DB)
│   ├── moderation.py     # Solo spam/flood/trolls
│   └── commands/
│       ├── start.py
│       ├── pregunta.py
│       ├── sticker.py
│       ├── encuesta.py   # /crear_encuesta admin-only
│       └── stats.py
├── services/
│   ├── grok_service.py
│   ├── sticker_service.py   # Límite diario en mem
│   └── moderation_service.py
└── middlewares/
    └── throttling.py
```

Sin models/, repositories/, infrastructure/.

---

## Cómo Agregar un Nuevo Comando (Ejemplo)

1. Crear `src/trinchera_bot/handlers/commands/mi_comando.py`
2. Definir `router = Router(name="mi_comando")`
3. `@router.message(Command("micomando"))`
4. En `application.py`:
   ```python
   from .handlers.commands import mi_comando
   dp.include_router(mi_comando.router)
   ```

El proyecto está diseñado para escalar sin dolor.

---

## Estructura del Proyecto

```
src/trinchera_bot/
├── constants.py          # Textos exactos + system prompt
├── config.py             # Pydantic Settings
├── main.py               # Entry polling
├── application.py        # Glue de routers + scheduler
├── bot.py
├── handlers/
│   ├── chat_member.py    # Bienvenida EXACTA
│   ├── moderation.py     # Anti-spam (sin censura política)
│   └── commands/
├── services/             # Grok, Sticker, Moderation, etc.
├── repositories/
├── models/               # SQLAlchemy
└── infrastructure/       # DB + Scheduler
```

---

## Notas Importantes sobre Moderación

El bot **nunca** elimina mensajes por:
- Opiniones políticas (aunque sean "viva Perón" o "Milei es un desastre")
- Debate fuerte pero con argumentos

Solo actúa sobre comportamiento tóxico claro (spam, flood, insultos personales, publicidad ajena).

---

## Costos (Versión Ligera)

- Principalmente API de Grok (xAI) para preguntas y stickers.
- Sin costos de base de datos.
- Muy barato de mantener.

---

## Licencia

MIT — Libertarian Voice 2026

---

## Cómo correr el bot (versión ligera)

### Comando exacto (Windows PowerShell, desde la raíz del proyecto):

```powershell
uv run python -m trinchera_bot.main
```

O si no usás uv:

```powershell
$env:PYTHONPATH="src"; python -m trinchera_bot.main
```

### Qué esperar al iniciarlo:
- Logs claros: "=== Iniciando Trinchera Libertaria Bot v1.0 ==="
- "🚀 Trinchera Bot (versión ligera SIN DB) iniciado"
- "Bot listo. Iniciando polling..."
- Comandos registrados en @BotFather (si tenés permisos)
- El bot responde a bienvenidas, moderación, /pregunta, /sticker, etc.
- Si falta alguna variable obligatoria del .env → Pydantic falla al arrancar (error claro).

### Cómo probar los comandos principales:

1. **Bienvenida automática**: Agregá un usuario de prueba (o cambiate de cuenta) al grupo Trinchera. Debe llegar el mensaje EXACTO de constants.WELCOME_HTML.

2. **/start y /ayuda**: En privado o en el grupo.

3. **/pregunta**: 
   ```
   /pregunta ¿por qué el socialismo siempre fracasa?
   ```
   Debe responder en estilo libertario con Grok (puede tardar 2-8 seg).

4. **/sticker**:
   ```
   /sticker león rugiendo rompiendo cadenas con la bandera de Gadsden
   ```
   Llega un sticker PNG 512x512. (Límite 3/día por usuario en memoria).

5. **/crear_encuesta** (solo desde cuenta admin):
   ```
   /crear_encuesta ¿Milei o Massa en 2023? | Milei | Massa | Abstención
   ```
   Crea poll en el grupo principal (o donde estés si sos admin).

6. **/stats** (solo admins):
   Muestra uptime + contadores de la sesión actual.

**Moderación**: Mandá spam ("gana dinero fácil"), flood (6 msgs seguidos), o insulto personal grave desde cuenta NO-admin → se borra + advertencia + posible mute 60min.

**Nunca** borra debate político.

---

**Viva la libertad, carajo.**

Bot simplificado y funcional. Sin lastre de base de datos.
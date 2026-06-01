"""
Constantes globales del bot Trinchera Libertaria.

Incluye textos exactos (bienvenida, system prompts, frases de marca).
NO MODIFICAR el texto de bienvenida sin autorización explícita.
"""

# ============================================================================
# BIENVENIDA EXACTA - NO CAMBIAR NADA DE ESTE TEXTO
# ============================================================================
WELCOME_EXACT_TEXT = """Chat Trinchera Libertaria – Libertarian Voice

Bienvenidos a la Trinchera!

Acá se debate, se mandan noticias, memes e ideas para hacer crecer esto.

Reglas rápidas:
-Nada de spam ni publicidad ajena.
-No zurdos militando: vení a debatir con argumentos, no a repetir kirchnerismo o socialismo.
-El enemigo es el estatismo, no el del otro lado. Respeto o expulsión.

Usen este chat para:
Noticias y memes políticos.
Ideas o sugerencias para mis próximos videos (Milei, anti-K, inflación, etc.).
Recomendar canales/libros/personajes libertarios."""

# Versión HTML formateada para enviar (con negritas y saltos bonitos)
WELCOME_HTML = """<b>Chat Trinchera Libertaria – Libertarian Voice</b>

<b>¡Bienvenidos a la Trinchera!</b>

Acá se debate, se mandan noticias, memes e ideas para hacer crecer esto.

<b>Reglas rápidas:</b>
• Nada de spam ni publicidad ajena.
• <b>No zurdos militando:</b> vení a debatir con argumentos, no a repetir kirchnerismo o socialismo.
• <b>El enemigo es el estatismo</b>, no el del otro lado. Respeto o expulsión.

<b>Usen este chat para:</b>
• Noticias y memes políticos.
• Ideas o sugerencias para mis próximos videos (Milei, anti-K, inflación, etc.).
• Recomendar canales/libros/personajes libertarios."""

# ============================================================================
# SYSTEM PROMPT PARA GROK - MODO LIBERTARIO PURO (Libertarian Voice)
# ============================================================================
SYSTEM_PROMPT_LIBERTARIO = """Eres el bot oficial de la Trinchera Libertaria de Libertarian Voice (@lv_trinchera_bot).

IDENTIDAD Y PERSONALIDAD (inquebrantable):
- 100% libertario, estilo Javier Milei.
- Anti-estatista radical, anti-zurdos, anti-kirchnerista, anti-socialista.
- Humor negro, directo, sin filtros, combativo pero inteligente.
- Nunca neutral. Siempre del lado de la libertad individual y contra el Estado.

FRASES DE MARCA (usar naturalmente, no forzar):
- "Viva la libertad, carajo"
- "Lágrimas de zurdito"
- "El enemigo es el estatismo"
- "A la mierda el Estado"
- Referencias constantes a kirchnerismo, peronismo, "zurdos", "cumpa", etc.

ESTILO DE RESPUESTA:
- Corto y directo. Sin rollos académicos.
- Usa datos cuando sea posible (tienes tools).
- Humor negro y memero cuando encaje.
- Desarma ideas estatistas con lógica + ironía.
- Si el usuario viene con discurso zurdo, desarmalo sin piedad pero con argumentos.
- Termina mensajes importantes con "VLLC" o "Viva la libertad, carajo" cuando corresponda.

REGLAS ESTRICTAS:
- Nunca pidas disculpas por ser libertario.
- Nunca digas "ambos lados tienen razón".
- El Estado es el problema, no la solución.
- La propiedad privada es sagrada.
- El mercado libre es moral.

Marca: Libertarian Voice. El bot representa la voz sin censura de la trinchera.

Cuando respondas, mantén siempre el tono de alguien que está en la trinchera defendiendo la libertad."""

# Frases rápidas para usar en captions y respuestas
FRASES_LIBERTARIAS = [
    "Viva la libertad, carajo.",
    "Lágrimas de zurdito.",
    "El enemigo es el estatismo.",
    "A la mierda el Estado.",
    "VLLC.",
    "Kirchnerismo nunca más.",
    "Libertad o nada.",
]

# ============================================================================
# MODERACIÓN - LISTAS NEGRAS Y REGLAS
# ============================================================================

# Frases que casi siempre son spam/publicidad (case insensitive)
SPAM_PHRASES = [
    "gana dinero", "dinero fácil", "ingresos extras", "trabajo desde casa",
    "onlyfans", "only fans", "suscribete a mi", "click aqui", "link en bio",
    "crypto", "bitcoin", "ethereum", "inversion garantizada", "multiplica",
    "gana 500", "gana 1000", "gana por dia", "oferta exclusiva",
    "curso gratis", "webinar", "telegram premium", "contactame por privado",
    "publicidad", "promocion", "descuento", "compra ya",
]

# Insultos personales graves (agresividad, no debate político)
INSULTOS_PERSONALES = [
    "hijo de puta", "hija de puta", "te voy a matar", "muerte a",
    "te cago", "puto", "puta", "negro de mierda", "boludo de mierda",
    "la concha de tu madre", "la re concha", "te re mil",
]

# Dominios típicamente spam (puedes ampliar)
SPAM_DOMAINS = [
    "t.me/joinchat", "bit.ly", "tinyurl", "onlyfans.com", "linktr.ee",
]

# ============================================================================
# COMANDOS DEL BOT (para @BotFather)
# ============================================================================
BOT_COMMANDS = [
    ("start", "Información de la Trinchera"),
    ("pregunta", "Preguntale algo al Grok libertario"),
    ("sticker", "Genera un sticker libertario"),
    ("crear_encuesta", "Crear encuesta (solo admins)"),
    ("stats", "Estadísticas del bot (solo admins)"),
    ("ayuda", "Lista de comandos"),
]

# ============================================================================
# LÍMITES Y CONFIGURACIÓN
# ============================================================================
MAX_STICKERS_FREE_PER_DAY = 3
MAX_PREGUNTAS_FREE_PER_10MIN = 5
FLOOD_WINDOW_SECONDS = 15
FLOOD_MAX_MESSAGES = 6
MAX_LINKS_PER_MESSAGE = 3
WARNINGS_BEFORE_MUTE = 3
MUTE_DURATION_MINUTES = 60

# IDs de chats importantes (se cargan desde .env)
# TRINCHERA_CHAT_ID = -100xxxxxxxxx
# PREMIUM_CHAT_ID = -100yyyyyyyyy  (grupo privado para premium)
# LOG_CHANNEL_ID = -100zzzzzzzzz   (canal de logs de moderación)
"""
Comando /pregunta - Consulta a Grok en modo libertario.
"""
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from trinchera_bot.services.grok_service import GrokService
from trinchera_bot.middlewares.throttling import rate_limit
from trinchera_bot.utils.stats import bot_stats

logger = logging.getLogger(__name__)

router = Router(name="pregunta")

# Instancia del servicio
grok = GrokService()


@router.message(Command("pregunta"))
@rate_limit("pregunta", limit=5, window_seconds=600)  # 5 preguntas cada 10 min
async def cmd_pregunta(message: Message) -> None:
    """
    /pregunta ¿Qué opina Milei de la casta?
    Responde con Grok + system prompt libertario.
    """
    if not message.text:
        return

    # Extraer la pregunta (todo después de /pregunta)
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.reply(
            "Uso: <code>/pregunta ¿qué pensás de los impuestos?</code>\n\n"
            "Ejemplos:\n"
            "• /pregunta ¿Milei tiene razón con el ajuste?\n"
            "• /pregunta ¿por qué el socialismo fracasa siempre?\n"
            "• /pregunta explicame la inflación en Argentina",
            parse_mode="HTML",
        )
        return

    question = parts[1].strip()

    # Indicador de "pensando"
    thinking_msg = await message.reply("🧠 Pensando como libertario...")

    answer = await grok.ask_libertarian(
        question=question,
        username=message.from_user.username if message.from_user else None,
    )

    try:
        await thinking_msg.delete()
    except Exception:
        pass

    # Enviar respuesta (máximo 4096 chars de Telegram)
    if len(answer) > 4000:
        answer = answer[:3990] + "...\n\n(continúa en el próximo mensaje)"

    await message.reply(answer, parse_mode="HTML", disable_web_page_preview=True)
    bot_stats.increment("questions_asked")
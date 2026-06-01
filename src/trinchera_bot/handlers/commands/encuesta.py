"""
Comando /crear_encuesta - Solo administradores.
Crea una encuesta en el chat de la Trinchera usando Telegram Polls nativo.
"""
import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from trinchera_bot.config import settings
from trinchera_bot.utils.stats import bot_stats

logger = logging.getLogger(__name__)

router = Router(name="encuesta")


def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("crear_encuesta"))
async def cmd_crear_encuesta(message: Message, bot: Bot) -> None:
    if not _is_admin(message.from_user.id if message.from_user else 0):
        await message.reply("🚫 Solo administradores pueden crear encuestas en la Trinchera.")
        return

    if not message.text:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2 or not parts[1].strip():
        await message.reply(
            "Uso: <code>/crear_encuesta ¿Pregunta de la encuesta? | Opción 1 | Opción 2 | Opción 3</code>\n\n"
            "Ejemplo:\n"
            "/crear_encuesta ¿Milei tiene razón con el ajuste? | Sí, total | Parcialmente | No, es un vende patria\n\n"
            "Mínimo 2 opciones, separadas por | .",
            parse_mode="HTML",
        )
        return

    raw = parts[1].strip()
    # Separar por |
    segments = [s.strip() for s in raw.split("|") if s.strip()]

    if len(segments) < 2:
        await message.reply(
            "⚠️ Necesitás al menos <b>2 opciones</b> separadas por <code>|</code>.\n"
            "Ej: /crear_encuesta ¿Te gusta la libertad? | Sí | Obvio"
        )
        return

    if len(segments) > 10:
        await message.reply("Máximo 10 opciones por encuesta.")
        return

    question = segments[0]
    options = segments[1:]

    # Determinar dónde enviar la encuesta
    target_chat = message.chat.id
    # Si el comando viene de privado o de otro chat, mandarla al grupo principal
    if message.chat.id != settings.TRINCHERA_CHAT_ID:
        target_chat = settings.TRINCHERA_CHAT_ID

    try:
        await bot.send_poll(
            chat_id=target_chat,
            question=question,
            options=options,
            is_anonymous=False,  # Votos públicos = más trinchera
            allows_multiple_answers=False,
        )
        bot_stats.increment("polls_created")
        logger.info(f"Encuesta creada por admin {message.from_user.id}: {question[:50]}...")

        if target_chat != message.chat.id:
            await message.reply(
                f"✅ Encuesta creada en el chat de la Trinchera.\n"
                f"\"{question[:80]}...\""
            )
    except Exception as e:
        logger.error(f"Error creando encuesta: {e}")
        await message.reply(
            "No se pudo crear la encuesta. Verificá que el bot tenga permisos de enviar mensajes y encuestas en el grupo."
        )

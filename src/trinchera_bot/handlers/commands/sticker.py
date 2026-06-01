"""
Comando /sticker - Genera stickers con Grok Imagine (xAI).
Versión ligera: límite diario en memoria (se resetea al reiniciar).
"""
import os
import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

from trinchera_bot.services.sticker_service import StickerService
from trinchera_bot.utils.stats import bot_stats
from trinchera_bot.constants import MAX_STICKERS_FREE_PER_DAY

logger = logging.getLogger(__name__)

router = Router(name="sticker")
sticker_service = StickerService()


@router.message(Command("sticker"))
async def cmd_sticker(message: Message, bot: Bot) -> None:
    if not message.text:
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.reply(
            "Uso: <code>/sticker león libertario con cadena rota</code>\n\n"
            f"Límite free: {MAX_STICKERS_FREE_PER_DAY} stickers por día (en memoria).\n"
            "Se resetea al reiniciar el bot.",
            parse_mode="HTML",
        )
        return

    prompt = parts[1].strip()

    thinking = await message.reply("🎨 Generando sticker libertario con Grok Imagine...")

    path = await sticker_service.generate_sticker(
        prompt=prompt,
        user_id=message.from_user.id if message.from_user else 0,
    )

    try:
        await thinking.delete()
    except Exception:
        pass

    if path is None:
        await message.reply(
            f"⏳ Límite diario de {MAX_STICKERS_FREE_PER_DAY} stickers alcanzado.\n"
            "Volvé mañana o reiniciá el bot para resetear contador."
        )
        return

    bot_stats.increment("stickers_generated")

    try:
        await message.reply_sticker(FSInputFile(path))
    except Exception as e:
        logger.error(f"Error enviando sticker: {e}")
        await message.reply("Sticker generado pero falló el envío. Probá de nuevo.")
    finally:
        try:
            os.remove(path)
        except Exception:
            pass
"""
Comando /stats - Estadísticas de la sesión actual (solo admins).
Sin base de datos: todo en memoria, se resetea al reiniciar el bot.
"""
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from trinchera_bot.config import settings
from trinchera_bot.utils.stats import bot_stats

router = Router(name="stats")


def _is_admin(user_id: int) -> bool:
    return user_id in settings.admin_ids


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if not message.from_user or not _is_admin(message.from_user.id):
        await message.reply("🚫 Solo administradores pueden ver /stats.")
        return

    s = bot_stats.to_dict()

    text = (
        "<b>📊 STATS TRINCHERA (memoria)</b>\n\n"
        f"⏱️ Uptime: <b>{s['uptime']}</b>\n\n"
        f"💬 Mensajes procesados: <b>{s['messages_processed']}</b>\n"
        f"🗑️ Mensajes moderados (spam/flood): <b>{s['messages_moderated']}</b>\n"
        f"❓ Preguntas a Grok: <b>{s['preguntas']}</b>\n"
        f"🎨 Stickers generados: <b>{s['stickers']}</b>\n"
        f"📊 Encuestas creadas: <b>{s['encuestas']}</b>\n\n"
        "<i>Sin PostgreSQL, sin Alembic, sin SQLAlchemy.</i>\n"
        "<i>Versión minimalista y funcional.</i>\n\n"
        "Viva la libertad, carajo."
    )

    await message.reply(text, parse_mode="HTML")
"""
Configuración central de la aplicación (routers + startup).
Versión minimalista sin base de datos ni scheduler.
"""
import logging
from aiogram import Dispatcher, Bot

from trinchera_bot.handlers import chat_member, moderation
from trinchera_bot.handlers.commands import (
    start,
    pregunta,
    sticker,
    stats,
    encuesta,
)

logger = logging.getLogger(__name__)


async def setup_application(dp: Dispatcher, bot: Bot) -> None:
    """
    Registra routers de la versión ligera (sin DB, sin scheduler).
    """

    # === Routers ===
    # chat_member events first (separate update type)
    dp.include_router(chat_member.router)
    # Commands BEFORE moderation: Command handlers must match in groups before the broad catch-all moderation handler
    dp.include_router(start.router)
    dp.include_router(pregunta.router)
    dp.include_router(sticker.router)
    dp.include_router(encuesta.router)
    dp.include_router(stats.router)
    # Moderation last: only non-command messages in the main Trinchera group
    dp.include_router(moderation.router)

    # === Startup / Shutdown ===
    @dp.startup()
    async def on_startup() -> None:
        logger.info("🚀 Trinchera Bot (versión ligera SIN DB) iniciado")
        logger.info("Bienvenida exacta + moderación spam/flood + /pregunta + /sticker + encuestas + stats")
        logger.info("Viva la libertad, carajo.")

    @dp.shutdown()
    async def on_shutdown() -> None:
        logger.info("Bot apagado. El estatismo sigue existiendo.")
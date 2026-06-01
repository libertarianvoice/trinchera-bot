"""
Punto de entrada principal del bot (modo polling).

Uso:
    python -m trinchera_bot.main

Para producción alta escala usar webhook.py + FastAPI.
"""
import asyncio
import logging
import sys

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from trinchera_bot.config import settings
from trinchera_bot.bot import create_bot
from trinchera_bot.application import setup_application


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO if not settings.DEBUG else logging.DEBUG,
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        stream=sys.stdout,
    )

    logger = logging.getLogger(__name__)
    logger.info("=== Iniciando Trinchera Libertaria Bot v1.0 ===")
    logger.info(f"Entorno: {settings.ENVIRONMENT}")
    logger.info(f"Chat Trinchera: {settings.TRINCHERA_CHAT_ID}")

    bot = await create_bot()
    dp = Dispatcher(storage=MemoryStorage())

    # Configurar routers, middlewares, scheduler, etc.
    await setup_application(dp, bot)

    # Iniciar polling
    logger.info("Bot listo. Iniciando polling...")
    await dp.start_polling(
        bot,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True,  # En producción podés cambiar esto
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot detenido por el usuario. Viva la libertad, carajo.")
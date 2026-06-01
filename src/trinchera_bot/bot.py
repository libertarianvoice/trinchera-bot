"""
Fábrica del bot y configuración de comandos.
"""
import logging
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from trinchera_bot.config import settings
from trinchera_bot.constants import BOT_COMMANDS

logger = logging.getLogger(__name__)


async def create_bot() -> Bot:
    """Crea la instancia del bot con configuración por defecto."""
    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    # Registrar comandos en el menú
    try:
        await bot.set_my_commands(commands=BOT_COMMANDS)
        logger.info("Comandos del bot registrados correctamente")
    except Exception as e:
        logger.warning(f"No se pudieron registrar los comandos: {e}")

    return bot
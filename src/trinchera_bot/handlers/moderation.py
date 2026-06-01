"""
Handler de moderación (se ejecuta sobre mensajes del grupo Trinchera).

Elimina SOLO spam, flood y trolls/insultos personales graves.
NUNCA toca admins ni debate político (aunque sea zurdo).
Comandos (/pregunta, /sticker, etc.) se saltan explícitamente para que funcionen en el grupo.
Sin base de datos: warnings y flood en memoria (se resetean al reiniciar).
"""
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from aiogram import Router, Bot, F
from aiogram.types import Message

from trinchera_bot.config import settings
from trinchera_bot.services.moderation_service import ModerationService
from trinchera_bot.utils.stats import bot_stats
from trinchera_bot.constants import WARNINGS_BEFORE_MUTE, MUTE_DURATION_MINUTES

logger = logging.getLogger(__name__)

router = Router(name="moderation")

# Instancia global del servicio
moderation_service = ModerationService()

# Warnings en memoria (por sesión). user_id -> count
_session_warnings: dict[int, int] = defaultdict(int)


@router.message(
    F.chat.id == settings.TRINCHERA_CHAT_ID,
    ~F.text.startswith("/"),
)
async def moderate_message(message: Message, bot: Bot) -> None:
    """
    Revisa mensajes del grupo (omite comandos para que /pregunta, /sticker etc. funcionen).
    Solo elimina spam/flood/trolls. Ignora admins y debate político.
    """
    if not message.from_user:
        return

    bot_stats.increment("messages_processed")

    # Ignorar admins completamente (nunca moderar admins)
    if message.from_user.id in settings.admin_ids:
        return

    should_delete, reason = await moderation_service.should_delete_message(message)

    if not should_delete:
        return

    # === ELIMINAR MENSAJE ===
    try:
        await message.delete()
    except Exception as e:
        logger.warning(f"No se pudo eliminar mensaje: {e}")
        return

    bot_stats.increment("messages_deleted")

    # Warnings en memoria (sesión actual)
    _session_warnings[message.from_user.id] += 1
    warnings = _session_warnings[message.from_user.id]

    # Advertencia estilo Trinchera
    warning_text = (
        f"⚠️ <b>Respeto o expulsión.</b>\n"
        f"@{message.from_user.username or message.from_user.first_name}, "
        f"este mensaje fue eliminado por <b>{reason}</b>.\n\n"
        f"El enemigo es el estatismo, no el del otro lado."
    )

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=warning_text,
            parse_mode="HTML",
        )
    except Exception:
        pass

    # Log opcional
    await moderation_service.log_moderation_action(
        bot, message.chat.id, message.from_user.id, reason
    )

    # Mute temporal si llega al límite en esta sesión
    if warnings >= WARNINGS_BEFORE_MUTE:
        try:
            until_date = int((datetime.utcnow() + timedelta(minutes=MUTE_DURATION_MINUTES)).timestamp())
            await bot.restrict_chat_member(
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                until_date=until_date,
                permissions={"can_send_messages": False},
            )
            await bot.send_message(
                message.chat.id,
                f"🔇 <b>{message.from_user.first_name}</b> silenciado {MUTE_DURATION_MINUTES} min "
                f"por acumular {WARNINGS_BEFORE_MUTE} advertencias.\n"
                f"Respeto o expulsión, carajo.",
                parse_mode="HTML",
            )
            _session_warnings[message.from_user.id] = 0  # reset después de mute
        except Exception as e:
            logger.error(f"No se pudo mutear: {e}")
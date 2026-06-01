"""
Handler de eventos de miembros del chat (bienvenida exacta + my_chat_member).

- welcome_new_member: vía ChatMemberUpdated (requiere bot admin en el grupo)
- welcome_new_members_fallback: vía message.new_chat_members (más confiable en algunos casos)

IMPORTANTE: El texto de bienvenida es EXACTO y está en constants.WELCOME_HTML.
No modificar sin autorización.
"""
import logging
from aiogram import Router, Bot, F
from aiogram.filters import IS_NOT_MEMBER, IS_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated, Message

from trinchera_bot.constants import WELCOME_HTML
from trinchera_bot.config import settings

logger = logging.getLogger(__name__)

router = Router(name="chat_member")


@router.chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER),
    F.chat.type.in_({"group", "supergroup"}),
    ~F.new_chat_member.user.is_bot,
)
async def welcome_new_member(event: ChatMemberUpdated, bot: Bot) -> None:
    """
    Envía el mensaje de bienvenida EXACTO cuando alguien se une a la Trinchera.

    Usa el texto oficial de Libertarian Voice. Sin base de datos.
    """
    user = event.new_chat_member.user

    try:
        await bot.send_message(
            chat_id=event.chat.id,
            text=WELCOME_HTML,
            parse_mode="HTML",
            disable_web_page_preview=True,
        )
        logger.info(f"Bienvenida enviada a nuevo miembro: {user.id} ({user.username or user.first_name})")
    except Exception as e:
        logger.error(f"Error enviando bienvenida: {e}")


@router.my_chat_member(
    ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER),
    F.chat.id == settings.TRINCHERA_CHAT_ID,
)
async def bot_added_to_group(event: ChatMemberUpdated, bot: Bot) -> None:
    """El bot fue agregado al grupo principal."""
    status = event.new_chat_member.status
    if status == "administrator":
        await bot.send_message(
            event.chat.id,
            "✅ ¡Gracias por hacerme admin de la Trinchera!\n"
            "Ahora puedo dar la bienvenida oficial y moderar como corresponde.\n\n"
            "<b>Viva la libertad, carajo.</b>",
            parse_mode="HTML",
        )
    elif status == "member":
        await bot.send_message(
            event.chat.id,
            "⚠️ Fui agregado como miembro normal. Necesito permisos de <b>administrador</b> "
            "(eliminar mensajes, banear usuarios y fijar mensajes) para funcionar correctamente.",
            parse_mode="HTML",
        )


@router.message(
    F.chat.type.in_({"group", "supergroup"}),
    F.new_chat_members,
)
async def welcome_new_members_fallback(message: Message, bot: Bot) -> None:
    """
    Fallback de bienvenida usando el mensaje de servicio 'new_chat_members'.
    Garantiza que la bienvenida funcione en grupos incluso si el evento chat_member
    no se entrega (ej. permisos del bot, configuraciones de privacidad).
    """
    for user in message.new_chat_members or []:
        if user.is_bot:
            continue
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=WELCOME_HTML,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )
            logger.info(
                f"Bienvenida (fallback) enviada a nuevo miembro: {user.id} ({user.username or user.first_name})"
            )
            break  # una sola bienvenida por evento de servicio
        except Exception as e:
            logger.error(f"Error enviando bienvenida fallback: {e}")


# TODO: agregar handler para cuando un admin promueve/degrada al bot
# TODO: cache de administradores del chat (actualizar en my_chat_member y chat_member de admins)
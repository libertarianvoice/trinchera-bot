"""
Comando /start y /ayuda.
"""
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from trinchera_bot.constants import WELCOME_HTML

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Mensaje de bienvenida / info básica."""
    await message.answer(
        WELCOME_HTML + "\n\n"
        "Comandos principales:\n"
        "• <b>/pregunta</b> tu duda → Grok en modo Milei\n"
        "• <b>/sticker</b> descripción → Sticker con IA\n"
        "• <b>/crear_encuesta</b> (solo admins)\n"
        "• <b>/stats</b> (solo admins)\n\n"
        "<i>Viva la libertad, carajo.</i>",
        parse_mode="HTML",
    )


@router.message(Command("ayuda", "help"))
async def cmd_ayuda(message: Message) -> None:
    """Lista de comandos disponibles."""
    text = (
        "<b>Comandos de la Trinchera (versión ligera)</b>\n\n"
        "/start — Bienvenida oficial\n"
        "/pregunta &lt;pregunta&gt; — Hablar con Grok libertario\n"
        "/sticker &lt;descripción&gt; — Genera sticker con Imagine\n"
        "/crear_encuesta ¿Q? | Sí | No — Solo admins\n"
        "/stats — Estadísticas de la sesión (admins)\n"
        "/ayuda — Este mensaje\n\n"
        "<i>Sin base de datos. Funcional y minimalista.</i>\n"
        "<i>Viva la libertad, carajo.</i>"
    )
    await message.reply(text, parse_mode="HTML")
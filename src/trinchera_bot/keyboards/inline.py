"""
Teclados inline reutilizables del bot Trinchera.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from trinchera_bot.config import settings


def get_premium_keyboard() -> InlineKeyboardMarkup:
    """
    Botones de pago Premium.

    Incluye Telegram Stars + links externos (Mercado Pago, etc.).
    """
    builder = InlineKeyboardBuilder()

    # Telegram Stars (pago nativo dentro de Telegram)
    builder.button(
        text="⭐ Pagar con Telegram Stars",
        callback_data="premium:pay_stars",
    )

    # Links externos
    builder.button(
        text="💳 Mercado Pago / Tienda",
        url=settings.MERCADOPAGO_LINK,
    )
    builder.button(
        text="🌐 Stripe / PayPal",
        url=settings.STRIPE_LINK,
    )

    builder.button(
        text="✅ Ya pagué (activar manual)",
        callback_data="premium:claim",
    )

    builder.adjust(1)  # Una columna
    return builder.as_markup()


def get_stats_refresh_keyboard() -> InlineKeyboardMarkup:
    """Botón para refrescar estadísticas."""
    builder = InlineKeyboardBuilder()
    builder.button(text="🔄 Actualizar", callback_data="stats:refresh")
    return builder.as_markup()
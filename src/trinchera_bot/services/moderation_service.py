"""
Servicio de moderación automática.

FILOSOFÍA:
- Solo elimina spam, publicidad ajena, flood y trolls/insultos personales.
- NUNCA censura opiniones políticas aunque sean comunistas, kirchneristas o "zurdas".
- El debate con argumentos está protegido aunque sea fuerte.

Estrategia: heurísticas conservadoras + listas negras claras.
"""
import re
import hashlib
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, Set

from aiogram.types import Message

from trinchera_bot.constants import (
    SPAM_PHRASES,
    INSULTOS_PERSONALES,
    SPAM_DOMAINS,
    MAX_LINKS_PER_MESSAGE,
    FLOOD_WINDOW_SECONDS,
    FLOOD_MAX_MESSAGES,
    WARNINGS_BEFORE_MUTE,
)
from trinchera_bot.config import settings

logger = logging.getLogger(__name__)


class ModerationService:
    """
    Motor de moderación.

    Usa caches en memoria (por proceso). Para alta escala reemplazar por Redis.
    """

    def __init__(self) -> None:
        # Flood: user_id -> lista de timestamps de mensajes recientes
        self._flood_tracker: Dict[int, list[datetime]] = defaultdict(list)

        # Mensajes repetidos: user_id -> set de hashes recientes
        self._recent_hashes: Dict[int, Set[str]] = defaultdict(set)

        # Whitelist de temas "políticos permitidos" (baja la agresividad de detección)
        self._political_keywords = {
            "milei", "kirchner", "peron", "socialismo", "comunismo", "libertad",
            "estatismo", "zurdo", "kuka", "cumpa", "macri", "cfk", "inflation",
            "impuestos", "estado", "mercado", "libre", "propiedad", "venezuela",
        }

    def _contains_spam_phrase(self, text: str) -> bool:
        text_lower = text.lower()
        return any(phrase in text_lower for phrase in SPAM_PHRASES)

    def _contains_insulto_personal(self, text: str) -> bool:
        text_lower = text.lower()
        return any(insulto in text_lower for insulto in INSULTOS_PERSONALES)

    def _too_many_links(self, text: str) -> bool:
        # Cuenta URLs simples
        url_pattern = r"https?://\S+|t\.me/\S+|www\.\S+"
        links = re.findall(url_pattern, text)
        return len(links) >= MAX_LINKS_PER_MESSAGE

    def _contains_spam_domain(self, text: str) -> bool:
        text_lower = text.lower()
        return any(domain in text_lower for domain in SPAM_DOMAINS)

    def _is_flood(self, user_id: int) -> bool:
        """Detecta flood (> FLOOD_MAX_MESSAGES en la ventana de tiempo)."""
        now = datetime.utcnow()
        cutoff = now - timedelta(seconds=FLOOD_WINDOW_SECONDS)

        # Limpiar mensajes viejos
        self._flood_tracker[user_id] = [
            ts for ts in self._flood_tracker[user_id] if ts > cutoff
        ]

        self._flood_tracker[user_id].append(now)
        return len(self._flood_tracker[user_id]) > FLOOD_MAX_MESSAGES

    def _is_repetitive(self, user_id: int, text: str) -> bool:
        """Detecta mensajes casi idénticos repetidos."""
        if not text or len(text) < 10:
            return False

        text_hash = hashlib.md5(text.lower().encode()).hexdigest()[:12]

        if text_hash in self._recent_hashes[user_id]:
            return True

        # Mantener solo los últimos 4 hashes
        self._recent_hashes[user_id].add(text_hash)
        if len(self._recent_hashes[user_id]) > 4:
            self._recent_hashes[user_id].pop()

        return False

    def _is_political_debate(self, text: str) -> bool:
        """Si menciona temas políticos de la trinchera, somos más permisivos."""
        text_lower = text.lower()
        return any(kw in text_lower for kw in self._political_keywords)

    async def should_delete_message(self, message: Message) -> tuple[bool, str]:
        """
        Decide si un mensaje debe ser eliminado.

        Returns:
            (debe_eliminar, razon)
        """
        if not message.text and not message.caption:
            return False, ""

        text = (message.text or message.caption or "").strip()

        # 1. Flood
        if self._is_flood(message.from_user.id):
            return True, "flood"

        # 2. Spam obvio
        if self._contains_spam_phrase(text) or self._contains_spam_domain(text):
            return True, "spam"

        # 3. Demasiados links
        if self._too_many_links(text):
            return True, "demasiados_links"

        # 4. Insultos personales graves (NO debate político)
        if self._contains_insulto_personal(text) and not self._is_political_debate(text):
            return True, "insulto_personal"

        # 5. Mensajes repetitivos
        if self._is_repetitive(message.from_user.id, text):
            return True, "repetitivo"

        return False, ""

    async def log_moderation_action(
        self,
        bot: "Bot",  # type: ignore
        chat_id: int,
        user_id: int,
        reason: str,
        deleted: bool = True,
    ) -> None:
        """Envía log al canal de moderación (si está configurado)."""
        if not settings.LOG_CHANNEL_ID:
            return

        try:
            reason_text = {
                "flood": "Flood (demasiados mensajes seguidos)",
                "spam": "Spam o publicidad ajena",
                "demasiados_links": "Exceso de enlaces",
                "insulto_personal": "Insulto personal / agresividad",
                "repetitivo": "Mensaje repetitivo",
            }.get(reason, reason)

            await bot.send_message(
                settings.LOG_CHANNEL_ID,
                f"🛡️ <b>Moderación</b>\n"
                f"Chat: <code>{chat_id}</code>\n"
                f"Usuario: <code>{user_id}</code>\n"
                f"Razón: {reason_text}\n"
                f"Acción: {'Mensaje eliminado' if deleted else 'Advertencia'}",
                parse_mode="HTML",
            )
        except Exception as e:
            logger.warning(f"No se pudo loguear moderación: {e}")
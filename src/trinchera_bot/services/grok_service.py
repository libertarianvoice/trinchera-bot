"""
Servicio de integración con Grok (xAI) en modo libertario.

Usa xai-sdk nativo (async).
"""
import logging
from typing import Optional

from xai_sdk import AsyncClient
from xai_sdk.chat import system, user

from trinchera_bot.config import settings
from trinchera_bot.constants import SYSTEM_PROMPT_LIBERTARIO

logger = logging.getLogger(__name__)


class GrokService:
    """Cliente Grok envuelto con personalidad de la Trinchera."""

    def __init__(self) -> None:
        self.client = AsyncClient(api_key=settings.XAI_API_KEY)
        self.model = "grok-4.3"  # Modelo principal 2026

    async def ask_libertarian(
        self,
        question: str,
        username: Optional[str] = None,
    ) -> str:
        """
        Realiza una pregunta a Grok con el system prompt libertario.

        Returns: respuesta en texto plano (listo para Telegram).
        """
        try:
            chat = self.client.chat.create(model=self.model)

            # System prompt de marca
            chat.append(system(SYSTEM_PROMPT_LIBERTARIO))

            # Contexto ligero del usuario
            if username:
                chat.append(
                    system(f"El usuario que pregunta se llama @{username}. Responde en español rioplatense.")
                )

            chat.append(user(question))

            response = await chat.sample()
            content = response.content.strip()

            # Asegurar que termine con algo de marca si no lo hace
            if not any(frase.lower() in content.lower() for frase in ["libertad", "carajo", "zurdo", "vllc"]):
                content += "\n\nViva la libertad, carajo."

            return content

        except Exception as e:
            logger.error(f"Error llamando a Grok: {e}")
            return (
                "Disculpá, el sistema de IA está peleando con un zurdito en este momento.\n"
                "Probá de nuevo en un minuto.\n\n"
                "Viva la libertad, carajo."
            )
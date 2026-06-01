"""
Generador de stickers con Grok Imagine.

Optimizado para formato Telegram (512x512, transparente, estilo sticker).
"""
import os
import tempfile
import logging
from io import BytesIO
from datetime import datetime

import httpx
from PIL import Image
from xai_sdk import AsyncClient

from trinchera_bot.config import settings
from trinchera_bot.constants import MAX_STICKERS_FREE_PER_DAY

logger = logging.getLogger(__name__)


class StickerService:
    def __init__(self) -> None:
        self.client = AsyncClient(api_key=settings.XAI_API_KEY)
        # Cache simple de uso por día (en memoria) - sin premium
        self._usage: dict[int, tuple[datetime, int]] = {}

    def _can_generate(self, user_id: int) -> bool:
        today = datetime.utcnow().date()
        last_date, count = self._usage.get(user_id, (today, 0))
        if last_date != today:
            self._usage[user_id] = (today, 0)
            return True
        return count < MAX_STICKERS_FREE_PER_DAY

    def _register_usage(self, user_id: int) -> None:
        today = datetime.utcnow().date()
        last_date, count = self._usage.get(user_id, (today, 0))
        if last_date != today:
            self._usage[user_id] = (today, 1)
        else:
            self._usage[user_id] = (today, count + 1)

    async def generate_sticker(self, prompt: str, user_id: int) -> str | None:
        """
        Genera un sticker y devuelve la ruta del archivo PNG listo para enviar.
        Límite diario en memoria para todos los usuarios.
        Devuelve None si alcanzó el límite.
        """
        if not self._can_generate(user_id):
            return None

        try:
            # Prompt engineering fuerte para stickers de Telegram
            full_prompt = (
                f"Telegram sticker style, thick bold black outlines, flat vibrant colors, "
                f"transparent background, centered composition, high contrast, clean vector look, "
                f"simple cartoon illustration, no text unless part of the joke, libertarian voice meme aesthetic, "
                f"{prompt}"
            )

            response = await self.client.image.sample(
                prompt=full_prompt,
                aspect_ratio="1:1",
            )

            # Descargar imagen
            async with httpx.AsyncClient(timeout=30.0) as client:
                img_resp = await client.get(response.url)
                img_resp.raise_for_status()

            # Procesar con Pillow → 512x512 RGBA PNG
            img = Image.open(BytesIO(img_resp.content))
            if img.mode != "RGBA":
                img = img.convert("RGBA")

            img = img.resize((512, 512), Image.Resampling.LANCZOS)

            # Guardar temporal
            tmp_path = os.path.join(tempfile.gettempdir(), f"sticker_{user_id}_{datetime.utcnow().timestamp()}.png")
            img.save(tmp_path, "PNG", optimize=True)

            self._register_usage(user_id)
            return tmp_path

        except Exception as e:
            logger.error(f"Error generando sticker: {e}")
            return None
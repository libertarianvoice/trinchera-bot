"""
Middleware de rate limiting simple (en memoria).

Para producción real se recomienda Redis + aiogram throttling.
"""
import time
from collections import defaultdict
from typing import Callable, Awaitable, Dict, Any
from functools import wraps

from aiogram.types import Message

# Almacenamiento simple por proceso
_user_last_calls: Dict[str, list[float]] = defaultdict(list)


def rate_limit(key: str, limit: int = 5, window_seconds: int = 60):
    """
    Decorador de rate limit por usuario.

    Ejemplo:
        @rate_limit("pregunta", limit=5, window_seconds=600)
    """

    def decorator(func: Callable[[Message], Awaitable[Any]]):
        @wraps(func)
        async def wrapper(message: Message, *args, **kwargs):
            if not message.from_user:
                return await func(message, *args, **kwargs)

            user_id = message.from_user.id
            cache_key = f"{key}:{user_id}"

            now = time.time()
            # Limpiar timestamps viejos
            _user_last_calls[cache_key] = [
                t for t in _user_last_calls[cache_key] if now - t < window_seconds
            ]

            if len(_user_last_calls[cache_key]) >= limit:
                await message.reply(
                    "⏳ Tranquilo, carajo. Estás yendo muy rápido.\n"
                    "Dale un poco de descanso al bot."
                )
                return

            _user_last_calls[cache_key].append(now)
            return await func(message, *args, **kwargs)

        return wrapper

    return decorator
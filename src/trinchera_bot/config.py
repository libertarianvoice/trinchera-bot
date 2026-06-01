"""
Configuración central del bot usando Pydantic Settings v2.

Todas las variables sensibles vienen de variables de entorno.
Nunca hardcodear tokens ni IDs aquí.
"""
from typing import Any, List
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración tipada y validada del bot Trinchera."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ========================================================================
    # TELEGRAM
    # ========================================================================
    BOT_TOKEN: str = Field(..., description="Token del bot de @BotFather")
    TRINCHERA_CHAT_ID: int = Field(
        ..., description="ID del grupo principal de la Trinchera (negativo)"
    )

    # ========================================================================
    # XAI / GROK
    # ========================================================================
    XAI_API_KEY: str = Field(..., description="API Key de xAI (Grok)")

    # ========================================================================
    # ADMINISTRADORES Y CHATS ESPECIALES
    # ========================================================================
    ADMIN_USER_IDS: List[int] = Field(
        default_factory=list,
        description="IDs de superadmins (acepta '123,456' string o lista [123,456] desde env/config)",
    )

    PREMIUM_CHAT_ID: int | None = Field(
        default=None,
        description="ID del grupo privado Premium (si existe)",
    )

    LOG_CHANNEL_ID: int | None = Field(
        default=None,
        description="Canal privado para logs de moderación (recomendado)",
    )

    # ========================================================================
    # YOUTUBE (para /noticias automático)
    # ========================================================================
    YOUTUBE_API_KEY: str | None = Field(
        default=None, description="Google Cloud YouTube Data API v3 key"
    )
    YOUTUBE_CHANNEL_ID: str = Field(
        default="UC_x5XG1OV2P6uZZ5FSM9Ttw",  # Placeholder - reemplazar por @LibertarianVoice real
        description="Channel ID del canal de YouTube de Libertarian Voice",
    )
    YOUTUBE_POLL_INTERVAL_MINUTES: int = Field(
        default=45, description="Cada cuántos minutos chequear videos nuevos"
    )

    # ========================================================================
    # PAGOS (Telegram Stars + links externos)
    # ========================================================================
    # Para Stars el provider_token queda vacío. Para otros proveedores se usa.
    PAYMENT_PROVIDER_TOKEN: str = Field(
        default="", description="Token de proveedor de pagos (vacío para Stars)"
    )
    PREMIUM_PRICE_STARS: int = Field(
        default=250, description="Precio en Telegram Stars del Premium"
    )
    MERCADOPAGO_LINK: str = Field(
        default="https://libertarianvoice.store",
        description="Link a checkout de Mercado Pago / tienda",
    )
    STRIPE_LINK: str = Field(
        default="https://libertarianvoice.store",
        description="Link alternativo Stripe/PayPal",
    )

    # ========================================================================
    # SEGURIDAD Y COMPORTAMIENTO
    # ========================================================================
    DEBUG: bool = Field(default=False)
    ENVIRONMENT: str = Field(default="production")  # development | production

    @field_validator("ADMIN_USER_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: Any) -> List[int]:
        """Convierte flexiblemente string '123,456' / '8155160091' o lista en List[int].

        Robusto: maneja vacíos, comas, espacios, listas de str/int, None, JSON array,
        valores sueltos. Siempre retorna list[int] (o []).
        """
        if v is None:
            return []

        if isinstance(v, (list, tuple)):
            items = list(v)
        elif isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            # Soporte extra para quien ponga JSON array en la variable de entorno
            if v.startswith("[") and v.endswith("]"):
                try:
                    import json

                    parsed = json.loads(v)
                    items = parsed if isinstance(parsed, (list, tuple)) else [parsed]
                except Exception:
                    inner = v[1:-1].strip()
                    items = [x.strip() for x in inner.split(",")] if inner else []
            else:
                items = [x.strip() for x in v.split(",")]
        elif isinstance(v, (int, float)) and not isinstance(v, bool):
            items = [int(v)]
        else:
            # último recurso: intentar como iterable
            try:
                items = list(v)
            except Exception:
                items = [v]

        # Normalizar cada elemento a int, saltando vacíos
        result: List[int] = []
        for x in items:
            if x is None:
                continue
            if isinstance(x, str):
                x = x.strip()
                if not x:
                    continue
            try:
                result.append(int(x))
            except (ValueError, TypeError):
                raise ValueError(
                    f"ADMIN_USER_IDS contiene valor no numérico: {x!r} (tipo {type(x).__name__})"
                ) from None

        return result

    @property
    def admin_ids(self) -> List[int]:
        """Lista de administradores superusuarios."""
        return self.ADMIN_USER_IDS

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() in ("dev", "development", "local")


# Instancia global de configuración
settings = Settings()


def get_settings() -> Settings:
    """Helper para inyección de dependencias futura."""
    return settings
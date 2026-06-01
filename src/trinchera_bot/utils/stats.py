"""
Estadísticas en memoria del bot (sin base de datos).
Se resetean al reiniciar el proceso. Suficiente para /stats de admins.
"""
import time
from dataclasses import dataclass, field


@dataclass
class BotStats:
    start_time: float = field(default_factory=time.time)
    messages_processed: int = 0
    messages_deleted: int = 0
    questions_asked: int = 0
    stickers_generated: int = 0
    polls_created: int = 0

    def uptime_seconds(self) -> int:
        return int(time.time() - self.start_time)

    def format_uptime(self) -> str:
        secs = self.uptime_seconds()
        hours, rem = divmod(secs, 3600)
        mins, secs = divmod(rem, 60)
        if hours > 0:
            return f"{hours}h {mins}m"
        if mins > 0:
            return f"{mins}m {secs}s"
        return f"{secs}s"

    def increment(self, metric: str) -> None:
        if hasattr(self, metric):
            setattr(self, metric, getattr(self, metric) + 1)

    def to_dict(self) -> dict:
        return {
            "uptime": self.format_uptime(),
            "messages_processed": self.messages_processed,
            "messages_moderated": self.messages_deleted,
            "preguntas": self.questions_asked,
            "stickers": self.stickers_generated,
            "encuestas": self.polls_created,
        }


# Singleton global (en memoria por proceso)
bot_stats = BotStats()

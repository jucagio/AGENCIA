from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, UTC


@dataclass
class Message:
    role: str
    content: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


class SessionService:
    """Historial de conversacion por (user_id, agent_name). Ventana deslizante."""

    def __init__(self, max_messages: int = 20) -> None:
        self._max = max_messages
        self._sessions: dict[tuple[int, str], list[Message]] = defaultdict(list)

    def add_message(self, user_id: int, agent: str, role: str, content: str) -> None:
        key = (user_id, agent)
        self._sessions[key].append(Message(role=role, content=content))
        if len(self._sessions[key]) > self._max:
            self._sessions[key] = self._sessions[key][-self._max:]

    def get_history(self, user_id: int, agent: str) -> list[dict[str, str]]:
        return [
            {"role": m.role, "content": m.content}
            for m in self._sessions[(user_id, agent)]
        ]

    def clear(self, user_id: int, agent: str) -> None:
        self._sessions.pop((user_id, agent), None)

    def clear_all(self, user_id: int) -> None:
        keys = [k for k in self._sessions if k[0] == user_id]
        for k in keys:
            del self._sessions[k]

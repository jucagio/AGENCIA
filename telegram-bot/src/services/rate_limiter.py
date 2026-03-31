import time
from collections import defaultdict, deque


class RateLimiter:
    """Sliding window rate limiter en memoria."""

    def __init__(self, max_messages: int, window_seconds: int) -> None:
        self._max = max_messages
        self._window = window_seconds
        self._timestamps: dict[int, deque[float]] = defaultdict(deque)

    def allow(self, user_id: int) -> bool:
        now = time.monotonic()
        window_start = now - self._window
        q = self._timestamps[user_id]

        # Eliminar timestamps fuera de la ventana
        while q and q[0] < window_start:
            q.popleft()

        if len(q) >= self._max:
            return False

        q.append(now)
        return True

"""In-memory rate limiting middleware.

Limits requests per IP address within a sliding 60-second window.
In production, replace with Redis-backed limiter for multi-process
deployments.
"""

import time
from collections import defaultdict

from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Sliding-window rate limiter per client IP."""

    def __init__(self, app, requests_per_minute: int = 30):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._request_log: dict[str, list[float]] = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        """Check rate limit before forwarding request."""
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()

        # Prune entries older than 60 seconds
        self._request_log[client_ip] = [
            ts for ts in self._request_log[client_ip] if now - ts < 60
        ]

        if len(self._request_log[client_ip]) >= self.requests_per_minute:
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": {
                        "code": "RATE_LIMIT_EXCEEDED",
                        "message": (
                            f"Too many requests. Limit is "
                            f"{self.requests_per_minute} per minute."
                        ),
                    },
                },
            )

        self._request_log[client_ip].append(now)
        response = await call_next(request)
        return response

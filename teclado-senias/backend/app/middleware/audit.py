"""Structured audit logging middleware.

Emits one JSON line per request to stdout. In production, pipe stdout
to a log aggregator (CloudWatch, Datadog, etc.).

SECURITY: Never logs request bodies, tokens, or PII.
"""

import logging
import time
from datetime import datetime, timezone

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("audit")


class AuditMiddleware(BaseHTTPMiddleware):
    """Log every HTTP request as structured JSON."""

    async def dispatch(self, request: Request, call_next):
        """Record method, path, status, and latency."""
        client_ip = request.client.host if request.client else "unknown"
        start = time.perf_counter()

        response = await call_next(request)

        elapsed_ms = round((time.perf_counter() - start) * 1000, 2)

        logger.info(
            "request",
            extra={
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "client_ip": client_ip,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": elapsed_ms,
            },
        )

        return response

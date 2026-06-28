# Logging middleware for FastAPI/MAF
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("maf.middleware")

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        return response

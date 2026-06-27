"""
HTTP client for the real OpenClaw agent.
"""

import httpx
from typing import Any, Dict

from app.config import get_settings

settings = get_settings()


class OpenClawClient:
    def __init__(self):
        self.endpoint = settings.openclaw_endpoint.rstrip("/")

    async def execute(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        if not self.endpoint:
            raise ValueError("OPENCLAW_ENDPOINT is not configured")

        payload = {"prompt": prompt, "context": context or {}}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.endpoint}/execute",
                json=payload
            )
            response.raise_for_status()
            return response.json()

    async def health(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{self.endpoint}/health")
            resp.raise_for_status()
            return resp.json()

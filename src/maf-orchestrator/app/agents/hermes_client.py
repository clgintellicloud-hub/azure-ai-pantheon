"""
HTTP client for the real Hermes agent.

In production, point HERMES_ENDPOINT to the deployed ACA URL.
In local dev with mocks, it points to the compose service (or localhost).
"""

import httpx
import os
from typing import Any, Dict

from app.config import get_settings

settings = get_settings()


class HermesClient:
    def __init__(self):
        self.endpoint = settings.hermes_endpoint.rstrip("/")

    async def execute(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Call the Hermes agent's /execute endpoint.
        Returns the full response dict from the agent.
        """
        if not self.endpoint:
            raise ValueError("HERMES_ENDPOINT is not configured")

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

"""Dapr-aware HTTP client for custom agent Container Apps."""

from typing import Any, Dict

import httpx


class DaprAgentClient:
    """Invoke an agent through Dapr service invocation or direct HTTP fallback."""

    def __init__(
        self,
        *,
        agent_name: str,
        endpoint: str,
        dapr_app_id: str,
        dapr_http_port: str = "",
        timeout_seconds: float = 60.0,
    ):
        self.agent_name = agent_name
        self.endpoint = endpoint.rstrip("/")
        self.dapr_app_id = dapr_app_id
        self.dapr_http_port = dapr_http_port
        self.timeout_seconds = timeout_seconds

    @property
    def use_dapr(self) -> bool:
        return bool(self.dapr_http_port and self.dapr_app_id)

    def invoke_url(self, method: str) -> str:
        method = method.lstrip("/")
        if self.use_dapr:
            return f"http://localhost:{self.dapr_http_port}/v1.0/invoke/{self.dapr_app_id}/method/{method}"
        if not self.endpoint:
            raise ValueError(f"{self.agent_name} endpoint is not configured")
        return f"{self.endpoint}/{method}"

    async def execute(self, prompt: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
        payload = {"prompt": prompt, "context": context or {}}
        async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
            response = await client.post(self.invoke_url("execute"), json=payload)
            response.raise_for_status()
            return response.json()

    async def health(self) -> Dict[str, Any]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.invoke_url("health"))
            response.raise_for_status()
            return response.json()

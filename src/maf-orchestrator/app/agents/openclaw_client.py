"""
HTTP/Dapr client for the OpenClaw agent.

In production, prefer Dapr service invocation with OPENCLAW_DAPR_APP_ID.
For local dev, direct OPENCLAW_ENDPOINT still works.
"""

from app.agents.dapr_agent_client import DaprAgentClient
from app.config import get_settings


class OpenClawClient(DaprAgentClient):
    def __init__(self):
        settings = get_settings()
        super().__init__(
            agent_name="openclaw",
            endpoint=settings.openclaw_endpoint,
            dapr_app_id=settings.openclaw_dapr_app_id,
            dapr_http_port=settings.dapr_http_port,
        )

"""
HTTP/Dapr client for the Hermes agent.

In production, prefer Dapr service invocation with HERMES_DAPR_APP_ID.
For local dev, direct HERMES_ENDPOINT still works.
"""

from app.agents.dapr_agent_client import DaprAgentClient
from app.config import get_settings


class HermesClient(DaprAgentClient):
    def __init__(self):
        settings = get_settings()
        super().__init__(
            agent_name="hermes",
            endpoint=settings.hermes_endpoint,
            dapr_app_id=settings.hermes_dapr_app_id,
            dapr_http_port=settings.dapr_http_port,
        )

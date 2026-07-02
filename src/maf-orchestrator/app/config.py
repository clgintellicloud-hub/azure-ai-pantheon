"""
Central configuration for the MAF Orchestrator.
All secrets/config come from environment variables (never hardcoded).
Follows security guidelines: use .env for local, Managed Identity + Key Vault in prod.
"""

import json
import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class RouteDecision:
    route: str
    agents: list[str]
    reasoning: str
    capabilities: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class RouteDefinition:
    agent: str | list[str]
    keywords: list[str]
    capabilities: list[str] = field(default_factory=list)

    @property
    def agents(self) -> list[str]:
        if isinstance(self.agent, list):
            return self.agent
        return [self.agent]


class RouteConfig:
    """Capability route table loaded from JSON for production-safe routing."""

    def __init__(self, routes: dict[str, RouteDefinition]):
        self.routes = routes

    @classmethod
    def default(cls) -> "RouteConfig":
        return cls(
            {
                "researcher": RouteDefinition(
                    agent="hermes",
                    keywords=["research", "literature", "market", "analyze", "analysis", "deep"],
                    capabilities=["research", "analysis", "planning"],
                ),
                "coder": RouteDefinition(
                    agent="hermes",
                    keywords=["code", "implement", "refactor", "test", "debug"],
                    capabilities=["software-development", "testing"],
                ),
                "executor": RouteDefinition(
                    agent="openclaw",
                    keywords=["execute", "act", "book", "send", "operate", "run"],
                    capabilities=["task-execution", "automation"],
                ),
                "reviewer": RouteDefinition(
                    agent="hermes",
                    keywords=["review", "critique", "audit", "validate"],
                    capabilities=["quality-review", "security-review"],
                ),
                "both": RouteDefinition(
                    agent=["hermes", "openclaw"],
                    keywords=["also", "and", "handoff"],
                    capabilities=["multi-agent"],
                ),
            }
        )

    @classmethod
    def from_json(cls, value: str | None) -> "RouteConfig":
        if not value:
            return cls.default()
        data = json.loads(value)
        routes: dict[str, RouteDefinition] = {}
        for name, config in data.items():
            routes[name] = RouteDefinition(
                agent=config["agent"],
                keywords=list(config.get("keywords", [])),
                capabilities=list(config.get("capabilities", [])),
            )
        return cls(routes)

    def resolve(self, prompt: str) -> RouteDecision:
        prompt_lower = prompt.lower()

        # Explicit multi-agent phrasing takes precedence when paired with any analytical/execution signal.
        if any(word in prompt_lower for word in self.routes.get("both", RouteDefinition([], [])).keywords):
            has_research = any(word in prompt_lower for word in self.routes.get("researcher", RouteDefinition([], [])).keywords)
            has_execution = any(word in prompt_lower for word in self.routes.get("executor", RouteDefinition([], [])).keywords)
            if has_research or has_execution:
                route = self.routes["both"]
                return RouteDecision(
                    route="both",
                    agents=route.agents,
                    reasoning="Matched multi-agent handoff keywords.",
                    capabilities=route.capabilities,
                )

        for name, route in self.routes.items():
            if name == "both":
                continue
            if any(keyword in prompt_lower for keyword in route.keywords):
                return RouteDecision(
                    route=name,
                    agents=route.agents,
                    reasoning=f"Matched route '{name}' by configured keywords.",
                    capabilities=route.capabilities,
                )

        fallback = self.routes.get("executor", RouteDefinition("openclaw", []))
        return RouteDecision(
            route="executor",
            agents=fallback.agents,
            reasoning="No route keyword matched; defaulted to executor.",
            capabilities=fallback.capabilities,
        )


@dataclass
class Settings:
    # Agent endpoints (for direct HTTP fallback when Dapr is not enabled)
    hermes_endpoint: str = "http://localhost:8081"
    openclaw_endpoint: str = "http://localhost:8082"

    # Dapr sidecar and app IDs for service invocation
    dapr_http_port: str = ""
    hermes_dapr_app_id: str = "hermes-agent"
    openclaw_dapr_app_id: str = "openclaw-agent"
    dapr_state_store: str = "workflow-state"
    dapr_pubsub: str = "agent-events"

    # Azure OpenAI / Foundry model config
    azure_openai_endpoint: str = ""
    azure_openai_deployment: str = "gpt-4o"
    foundry_endpoint: str = ""
    model_name: str = "gpt-4o"

    # Cosmos DB for MAF state + checkpointing
    cosmos_endpoint: str = ""
    cosmos_key: str = ""
    cosmos_database: str = "pantheon"
    cosmos_container: str = "workflow_state"
    use_cosmos_state: bool = False

    # Capability routing table
    route_config_json: str = ""

    # Optional shared secret for inbound webhook HMAC-SHA256 validation.
    # SECURITY: Configure through Key Vault/app settings; never commit real values.
    webhook_shared_secret: str = ""

    @property
    def route_config(self) -> RouteConfig:
        return RouteConfig.from_json(self.route_config_json)


def get_settings() -> Settings:
    model_name = os.getenv("MODEL_NAME", "gpt-4o")
    cosmos_endpoint = os.getenv("COSMOS_ENDPOINT", "")
    return Settings(
        hermes_endpoint=os.getenv("HERMES_ENDPOINT", "http://localhost:8081"),
        openclaw_endpoint=os.getenv("OPENCLAW_ENDPOINT", "http://localhost:8082"),
        dapr_http_port=os.getenv("DAPR_HTTP_PORT", ""),
        hermes_dapr_app_id=os.getenv("HERMES_DAPR_APP_ID", "hermes-agent"),
        openclaw_dapr_app_id=os.getenv("OPENCLAW_DAPR_APP_ID", "openclaw-agent"),
        dapr_state_store=os.getenv("DAPR_STATE_STORE", "workflow-state"),
        dapr_pubsub=os.getenv("DAPR_PUBSUB", "agent-events"),
        azure_openai_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        azure_openai_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", model_name),
        foundry_endpoint=os.getenv("FOUNDRY_ENDPOINT", ""),
        model_name=model_name,
        cosmos_endpoint=cosmos_endpoint,
        cosmos_key=os.getenv("COSMOS_KEY", ""),
        cosmos_database=os.getenv("COSMOS_DATABASE", "pantheon"),
        cosmos_container=os.getenv("COSMOS_CONTAINER", "workflow_state"),
        use_cosmos_state=bool(os.getenv("USE_COSMOS_STATE", "false").lower() == "true") or bool(cosmos_endpoint),
        route_config_json=os.getenv("ROUTE_CONFIG_JSON", ""),
        webhook_shared_secret=os.getenv("WEBHOOK_SHARED_SECRET", ""),
    )


# Global settings instance (can be overridden in tests)
settings = get_settings()

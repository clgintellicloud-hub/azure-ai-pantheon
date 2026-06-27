"""
Central configuration for the MAF Orchestrator.
All secrets/config come from environment variables (never hardcoded).
Follows security guidelines: use .env for local, Managed Identity + Key Vault in prod.
"""

import os
from dataclasses import dataclass

@dataclass
class Settings:
    # Agent endpoints (for calling Hermes/OpenClaw)
    hermes_endpoint: str = os.getenv("HERMES_ENDPOINT", "http://localhost:8081")
    openclaw_endpoint: str = os.getenv("OPENCLAW_ENDPOINT", "http://localhost:8082")

    # Microsoft Foundry / Models (for future LLM planner)
    foundry_endpoint: str = os.getenv("FOUNDRY_ENDPOINT", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o")

    # Cosmos DB for MAF state + checkpointing
    # For Azure: use Managed Identity (no key needed)
    # For local / emulator: provide COSMOS_ENDPOINT and COSMOS_KEY (or use emulator defaults)
    cosmos_endpoint: str = os.getenv("COSMOS_ENDPOINT", "")
    cosmos_key: str = os.getenv("COSMOS_KEY", "")  # Only for local dev/emulator. Never commit real keys.
    cosmos_database: str = os.getenv("COSMOS_DATABASE", "pantheon")
    cosmos_container: str = os.getenv("COSMOS_CONTAINER", "workflow_state")

    # Whether to enable real Cosmos persistence (fallback to in-memory if false or no endpoint)
    use_cosmos_state: bool = bool(os.getenv("USE_COSMOS_STATE", "false").lower() == "true") or bool(cosmos_endpoint)

def get_settings() -> Settings:
    return Settings()

# Global settings instance (can be overridden in tests)
settings = get_settings()

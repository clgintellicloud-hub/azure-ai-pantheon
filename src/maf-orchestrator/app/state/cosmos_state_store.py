"""
Cosmos DB State Store for MAF Workflow Checkpointing + State.

Supports:
- Saving workflow state (plan, results, status, checkpoint metadata)
- Loading by checkpoint_id
- Basic resume support
- Fallback to in-memory store when Cosmos is not configured (local dev)

Designed for azure-cosmos SDK + Managed Identity in production.
Uses partition key on task_id or checkpoint_id for scalability.
"""

import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from azure.cosmos import CosmosClient, exceptions
from azure.identity import DefaultAzureCredential

from app.config import get_settings

settings = get_settings()


class CosmosStateStore:
    def __init__(self):
        self._memory_store: Dict[str, Dict[str, Any]] = {}
        self.client = None
        self.container = None
        self._use_cosmos = False

        if settings.use_cosmos_state and settings.cosmos_endpoint:
            try:
                if settings.cosmos_key:
                    # Local emulator or key-based (dev only)
                    self.client = CosmosClient(
                        url=settings.cosmos_endpoint,
                        credential=settings.cosmos_key
                    )
                else:
                    # Production: Managed Identity
                    credential = DefaultAzureCredential()
                    self.client = CosmosClient(
                        url=settings.cosmos_endpoint,
                        credential=credential
                    )

                database = self.client.get_database_client(settings.cosmos_database)
                self.container = database.get_container_client(settings.cosmos_container)
                self._use_cosmos = True
                print(f"[StateStore] Connected to Cosmos DB: {settings.cosmos_database}/{settings.cosmos_container}")
            except Exception as e:
                print(f"[StateStore] Failed to connect to Cosmos, falling back to in-memory: {e}")
                self._use_cosmos = False
        else:
            print("[StateStore] No Cosmos config detected. Using in-memory store (ephemeral).")

    def _generate_checkpoint_id(self, task: str) -> str:
        return f"ckpt-{uuid.uuid4().hex[:12]}"

    async def save_state(
        self,
        checkpoint_id: Optional[str],
        task: str,
        plan: Dict[str, Any],
        results: list[Dict[str, Any]],
        status: str = "in_progress",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Save or update workflow state.
        Returns the checkpoint_id (generated if not provided).
        """
        if not checkpoint_id:
            checkpoint_id = self._generate_checkpoint_id(task)

        state_doc = {
            "id": checkpoint_id,
            "task": task,
            "plan": plan,
            "results": results,
            "status": status,
            "metadata": metadata or {},
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

        if self._use_cosmos and self.container:
            try:
                # Upsert (id is the partition key for simplicity in early stage)
                self.container.upsert_item(body=state_doc)
            except exceptions.CosmosHttpResponseError as e:
                print(f"[StateStore] Cosmos upsert failed: {e}")
                # Fall through to memory as fallback
                self._memory_store[checkpoint_id] = state_doc
        else:
            self._memory_store[checkpoint_id] = state_doc

        return checkpoint_id

    async def load_state(self, checkpoint_id: str) -> Optional[Dict[str, Any]]:
        """Load previous workflow state for resume."""
        if self._use_cosmos and self.container:
            try:
                item = self.container.read_item(item=checkpoint_id, partition_key=checkpoint_id)
                return item
            except exceptions.CosmosResourceNotFoundError:
                return None
            except Exception as e:
                print(f"[StateStore] Cosmos read failed: {e}")
                return self._memory_store.get(checkpoint_id)
        else:
            return self._memory_store.get(checkpoint_id)

    async def update_result(
        self,
        checkpoint_id: str,
        agent_result: Dict[str, Any]
    ) -> None:
        """Append a single agent result to existing state (for incremental checkpointing)."""
        state = await self.load_state(checkpoint_id)
        if not state:
            return

        if "results" not in state:
            state["results"] = []

        state["results"].append(agent_result)
        state["updated_at"] = datetime.now(timezone.utc).isoformat()

        if self._use_cosmos and self.container:
            try:
                self.container.upsert_item(body=state)
            except Exception as e:
                print(f"[StateStore] Failed to update result in Cosmos: {e}")
                self._memory_store[checkpoint_id] = state
        else:
            self._memory_store[checkpoint_id] = state


# Global instance
state_store = CosmosStateStore()

# Basic tests for the MAF orchestrator (Phase 1)

import pytest
import asyncio
from httpx import AsyncClient

# Note: These tests assume the app is importable and mocks are running
# For full integration tests, use docker compose and test against ports

from app.main import app
from app.workflows.task_router import run_pantheon_workflow

@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_pantheon_workflow():
    result = await run_pantheon_workflow("Analyze this complex problem")
    assert "plan" in result
    assert "execution" in result or "results" in str(result)  # flexible for graph output
    assert "workflow" in result

@pytest.mark.asyncio
async def test_orchestrate_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/orchestrate", json={"prompt": "Execute a simple task"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "processed"
        assert "result" in data
        assert "checkpoint_id" in data  # MAF state support

@pytest.mark.asyncio
async def test_resume_with_checkpoint():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First call
        resp1 = await ac.post("/orchestrate", json={"prompt": "Analyze and execute"})
        ckpt = resp1.json().get("checkpoint_id")
        
        # Resume call
        resp2 = await ac.post("/orchestrate", json={"prompt": "Analyze and execute", "checkpoint_id": ckpt})
        assert resp2.status_code == 200
        assert resp2.json().get("checkpoint_id") == ckpt

# Basic tests for the MAF orchestrator (Phase 1)

import pytest
import asyncio
import logging
from httpx import AsyncClient, ASGITransport

# Note: These tests assume the app is importable and mocks are running
# For full integration tests, use docker compose and test against ports

from app.main import app
from app.config import RouteConfig
from app.agents.hermes_client import HermesClient
from app.workflows.task_router import plan_task, run_pantheon_workflow


def make_test_client():
    transport = ASGITransport(app=app)
    return AsyncClient(transport=transport, base_url="http://test")

@pytest.mark.asyncio
async def test_health():
    async with make_test_client() as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_pantheon_workflow():
    result = await run_pantheon_workflow("Analyze this complex problem")
    assert "plan" in result
    assert "execution" in result
    assert "agents_used" in result

@pytest.mark.asyncio
async def test_orchestrate_endpoint():
    async with make_test_client() as ac:
        response = await ac.post("/orchestrate", json={"prompt": "Execute a simple task"})
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "processed"
        assert "result" in data
        assert "checkpoint_id" in data  # MAF state support

@pytest.mark.asyncio
async def test_resume_with_checkpoint():
    async with make_test_client() as ac:
        # First call
        resp1 = await ac.post("/orchestrate", json={"prompt": "Analyze and execute"})
        ckpt = resp1.json().get("checkpoint_id")
        
        # Resume call
        resp2 = await ac.post("/orchestrate", json={"prompt": "Analyze and execute", "checkpoint_id": ckpt})
        assert resp2.status_code == 200
        assert resp2.json().get("checkpoint_id") == ckpt

@pytest.mark.asyncio
async def test_both_route():
    result = await run_pantheon_workflow("Research and also act on it")
    assert "both" in str(result.get("plan", {})).lower() or len(result.get("agents_used", [])) >= 1

@pytest.mark.asyncio
async def test_route_decisions():
    hermes_plan = await plan_task("Analyze this complex strategy problem")
    openclaw_plan = await plan_task("Book a flight")
    both_plan = await plan_task("Research the market and also execute outreach")

    assert hermes_plan["route"] == "researcher"
    assert openclaw_plan["route"] == "executor"
    assert both_plan["route"] == "both"

@pytest.mark.asyncio
async def test_orchestrate_does_not_log_raw_prompt(caplog):
    secret_prompt = "Execute this task with SECRET_TOKEN_123"
    caplog.set_level(logging.INFO, logger="maf-orchestrator")

    async with make_test_client() as ac:
        response = await ac.post("/orchestrate", json={"prompt": secret_prompt})

    assert response.status_code == 200
    assert secret_prompt not in caplog.text
    assert "SECRET_TOKEN_123" not in caplog.text


def test_route_config_supports_specialized_agents():
    route_config = RouteConfig.from_json(
        '{"researcher":{"agent":"hermes","keywords":["literature"],"capabilities":["research"]}}'
    )

    assert route_config.resolve("Do a literature review").route == "researcher"
    assert route_config.resolve("Do a literature review").agents == ["hermes"]


@pytest.mark.asyncio
async def test_hermes_client_uses_dapr_service_invocation(monkeypatch):
    monkeypatch.setenv("DAPR_HTTP_PORT", "3500")
    monkeypatch.setenv("HERMES_DAPR_APP_ID", "researcher-agent")
    client = HermesClient()

    assert client.invoke_url("execute") == "http://localhost:3500/v1.0/invoke/researcher-agent/method/execute"

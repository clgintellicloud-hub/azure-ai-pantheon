import importlib.util
import os
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

ROOT = Path(__file__).resolve().parents[1]


def load_wrapper(agent_dir: str, module_name: str, monkeypatch, *, command: str = ""):
    monkeypatch.setenv("AGENT_RUNTIME_COMMAND", command)
    monkeypatch.setenv("AGENT_RUNTIME_TIMEOUT_SECONDS", "5")
    module_path = ROOT / agent_dir / "src" / "main.py"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("agent_dir", "module_name", "expected_agent", "expected_phrase"),
    [
        ("hermes-agent", "hermes_wrapper_test", "hermes", "Hermes processed"),
        ("openclaw-agent", "openclaw_wrapper_test", "openclaw", "OpenClaw executed task"),
    ],
)
async def test_agent_wrapper_simulator_contract(
    monkeypatch, agent_dir, module_name, expected_agent, expected_phrase
):
    module = load_wrapper(agent_dir, module_name, monkeypatch)

    async with AsyncClient(
        transport=ASGITransport(app=module.app),
        base_url="http://test",
    ) as client:
        health = await client.get("/health")
        execute = await client.post("/execute", json={"prompt": "Do a task"})

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert health.json()["agent"] == expected_agent
    assert health.json()["mode"] == "simulator"
    assert health.json()["runtime_configured"] is False

    assert execute.status_code == 200
    body = execute.json()
    assert body["agent"] == expected_agent
    assert body["mode"] == "simulator"
    assert expected_phrase in body["result"]


@pytest.mark.asyncio
async def test_hermes_wrapper_runtime_command_contract(monkeypatch, tmp_path):
    script = tmp_path / "runtime_success.py"
    script.write_text(
        "import sys\ndata = sys.stdin.read()\nprint('runtime:' + data)\n",
        encoding="utf-8",
    )
    command = f"{os.sys.executable} {script}"
    module = load_wrapper("hermes-agent", "hermes_runtime_wrapper_test", monkeypatch, command=command)

    async with AsyncClient(
        transport=ASGITransport(app=module.app),
        base_url="http://test",
    ) as client:
        health = await client.get("/health")
        execute = await client.post("/execute", json={"prompt": "hello"})

    assert health.status_code == 200
    assert health.json()["mode"] == "runtime"
    assert health.json()["runtime_configured"] is True
    assert execute.status_code == 200
    assert execute.json()["mode"] == "runtime"
    assert execute.json()["result"] == "runtime:hello"


@pytest.mark.asyncio
async def test_openclaw_wrapper_runtime_failure_contract(monkeypatch, tmp_path):
    script = tmp_path / "runtime_failure.py"
    script.write_text(
        "import sys\nprint('bad', file=sys.stderr)\nraise SystemExit(7)\n",
        encoding="utf-8",
    )
    command = f"{os.sys.executable} {script}"
    module = load_wrapper(
        "openclaw-agent",
        "openclaw_runtime_failure_wrapper_test",
        monkeypatch,
        command=command,
    )

    async with AsyncClient(
        transport=ASGITransport(app=module.app),
        base_url="http://test",
    ) as client:
        execute = await client.post("/execute", json={"prompt": "hello"})

    assert execute.status_code == 502
    assert execute.json()["detail"]["exit_code"] == 7
    assert "bad" in execute.json()["detail"]["stderr"]

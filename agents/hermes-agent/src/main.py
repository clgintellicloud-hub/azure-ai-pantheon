# Hermes Agent HTTP wrapper for local mocks and real runtime commands.
# SECURITY: Runtime command and secrets come from environment variables only.

import asyncio
import os
import shlex
from typing import Any

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

AGENT_NAME = os.getenv("AGENT_NAME", "hermes")
RUNTIME_COMMAND = os.getenv("AGENT_RUNTIME_COMMAND", "").strip()
RUNTIME_TIMEOUT_SECONDS = float(os.getenv("AGENT_RUNTIME_TIMEOUT_SECONDS", "60"))

app = FastAPI(title="Hermes Agent Wrapper")


class TaskRequest(BaseModel):
    prompt: str
    context: dict[str, Any] = Field(default_factory=dict)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "agent": AGENT_NAME,
        "mode": "runtime" if RUNTIME_COMMAND else "simulator",
        "runtime_configured": bool(RUNTIME_COMMAND),
    }


@app.post("/execute")
async def execute(request: TaskRequest):
    if RUNTIME_COMMAND:
        return await execute_runtime(request)

    return {
        "agent": AGENT_NAME,
        "mode": "simulator",
        "result": f"Hermes processed: {request.prompt} [with skills and memory]",
        "plan": ["analyze", "act", "learn"],
        "confidence": 0.92,
    }


async def execute_runtime(request: TaskRequest) -> dict[str, Any]:
    """Run the configured runtime command with the prompt on stdin."""
    try:
        process = await asyncio.create_subprocess_exec(
            *shlex.split(RUNTIME_COMMAND, posix=os.name != "nt"),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(request.prompt.encode("utf-8")),
            timeout=RUNTIME_TIMEOUT_SECONDS,
        )
    except asyncio.TimeoutError as exc:
        raise HTTPException(status_code=504, detail="Hermes runtime timed out") from exc
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="Hermes runtime command not found") from exc

    stdout_text = stdout.decode("utf-8", errors="replace").strip()
    stderr_text = stderr.decode("utf-8", errors="replace").strip()

    if process.returncode != 0:
        raise HTTPException(
            status_code=502,
            detail={
                "message": "Hermes runtime failed",
                "exit_code": process.returncode,
                "stderr": stderr_text[-2000:],
            },
        )

    return {
        "agent": AGENT_NAME,
        "mode": "runtime",
        "status": "completed",
        "result": stdout_text,
    }

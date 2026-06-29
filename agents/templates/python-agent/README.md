# Base Python Agent Template

This template is the starting point for specialized containerized agents such as Researcher, Coder, Executor, and Reviewer. It preserves the orchestrator contract used by Hermes/OpenClaw wrappers.

## Contract

```http
GET /health
POST /execute
{
  "prompt": "...",
  "context": {}
}
```

## Specialization

Set these environment variables per Container App:

```text
AGENT_NAME=researcher-agent
AGENT_ROLE=researcher
AGENT_CAPABILITIES=research,analysis,planning
AGENT_RUNTIME_COMMAND=
AGENT_RUNTIME_TIMEOUT_SECONDS=60
```

When `AGENT_RUNTIME_COMMAND` is blank, the agent returns a deterministic simulator response for smoke tests. When configured, the prompt is passed to the runtime command on stdin and stdout becomes the result.

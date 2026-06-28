# Common tools for MAF
from typing import Dict, Any

async def log_tool_call(tool_name: str, args: Dict[str, Any]) -> None:
    print(f"Tool call: {tool_name} with {args}")

from __future__ import annotations

import json
import os
from urllib.request import Request, urlopen


def write_note_memory(note: dict, event_type: str) -> None:
    base_url = os.getenv("EVEROS_BASE_URL", "").rstrip("/")
    if not base_url:
        raise RuntimeError("EVEROS_BASE_URL is not configured")

    path = os.getenv("EVEROS_MEMORY_PATH", "/api/memories")
    token = os.getenv("EVEROS_API_TOKEN", "")
    space = os.getenv("FENGVOICE_MEMORY_SPACE", "fengvoice_engineering")
    action = "创建" if event_type == "note_created" else "更新"
    payload = {
        "space": space,
        "type": event_type,
        "content": f"用户{action}了 FengVoice 笔记：{note['title']}",
        "metadata": {"note_id": note["id"], "note_type": note["note_type"], "tags": note["tags"]},
    }
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"{base_url}{path}", data=json.dumps(payload, ensure_ascii=False).encode("utf-8"), headers=headers, method="POST")
    with urlopen(request, timeout=3) as response:
        if response.status >= 400:
            raise RuntimeError(f"EverCore returned HTTP {response.status}")


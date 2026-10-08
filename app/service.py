from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .store import load_tasks, next_task_id, save_tasks


def list_tasks(status: str | None = None, q: str | None = None) -> list[dict[str, Any]]:
    """Return task records, optionally filtered by status and search text."""
    tasks = load_tasks()
    filtered: list[dict[str, Any]] = []

    for task in tasks:
        if status and task["status"] != status:
            continue
        if q and q.lower() not in task["title"].lower() and q.lower() not in task["description"].lower():
            continue
        filtered.append(task)

    return filtered


def get_task(task_id: int) -> dict[str, Any] | None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            return task
    return None


def create_task(title: str, description: str, priority: str) -> dict[str, Any]:
    tasks = load_tasks()
    task = {
        "id": next_task_id(tasks),
        "title": title,
        "description": description,
        "status": "open",
        "priority": priority,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": None,
    }
    tasks.append(task)
    save_tasks(tasks)
    return task


def complete_task(task_id: int) -> dict[str, Any] | None:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            task["completed_at"] = datetime.now(timezone.utc).isoformat()
            save_tasks(tasks)
            return task
    return None

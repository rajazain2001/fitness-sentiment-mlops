"""MongoDB persistence for fitness sentiment analyses — Zain, Usama, Ali."""
import os
from datetime import datetime, timezone
from multiprocessing import Process, Queue
from typing import Any

AUTHORS = "Zain, Usama, Ali"

# Short timeouts everywhere so the Gradio worker never hangs.
_CLIENT_OPTS = {
    "serverSelectionTimeoutMS": 3000,
    "connectTimeoutMS": 3000,
    "socketTimeoutMS": 8000,
    "waitQueueTimeoutMS": 3000,
    "maxPoolSize": 5,
}

_PROCESS_TIMEOUT_SEC = 10


def is_db_configured() -> bool:
    return bool(os.getenv("MONGODB_URI", "").strip())


def _db_names() -> tuple[str, str]:
    return (
        os.getenv("MONGODB_DB_NAME", "fitness_app"),
        os.getenv("MONGODB_COLLECTION", "analyses"),
    )


def _worker_fetch(uri: str, db_name: str, coll_name: str, limit: int, out: Queue) -> None:
    try:
        from pymongo import MongoClient

        client = MongoClient(uri, **_CLIENT_OPTS)
        client.admin.command("ping")
        coll = client[db_name][coll_name]
        records = (
            coll.find()
            .sort("created_at", -1)
            .limit(limit)
            .max_time_ms(8000)
        )
        rows = []
        for doc in records:
            rows.append(
                {
                    "time": doc.get("created_at", ""),
                    "name": doc.get("display_name") or "—",
                    "text": (doc.get("text") or "")[:80],
                    "sentiment": doc.get("dominant_sentiment", ""),
                    "workout": doc.get("workout_mode", ""),
                    "confidence": doc.get("confidence_pct", ""),
                }
            )
        out.put(("ok", rows))
    except Exception as exc:
        out.put(("err", str(exc)))


def _worker_insert(uri: str, db_name: str, coll_name: str, doc: dict, out: Queue) -> None:
    try:
        from pymongo import MongoClient

        client = MongoClient(uri, **_CLIENT_OPTS)
        client.admin.command("ping")
        coll = client[db_name][coll_name]
        inserted = coll.insert_one(doc)
        out.put(("ok", str(inserted.inserted_id)))
    except Exception as exc:
        out.put(("err", str(exc)))


def _run_isolated(worker, *args) -> Any:
    """Run DB work in a child process so timeouts cannot freeze Gradio."""
    queue: Queue = Queue()
    proc = Process(target=worker, args=(*args, queue))
    proc.start()
    proc.join(timeout=_PROCESS_TIMEOUT_SEC)
    if proc.is_alive():
        proc.terminate()
        proc.join(2)
        raise TimeoutError(
            f"Database operation timed out after {_PROCESS_TIMEOUT_SEC} seconds."
        )
    if queue.empty():
        raise RuntimeError("Database worker exited without a result.")
    status, payload = queue.get()
    if status == "err":
        raise RuntimeError(payload)
    return payload


def save_analysis(raw_text: str, result: dict, display_name: str | None = None) -> dict[str, Any]:
    uri = os.environ.get("MONGODB_URI", "").strip()
    if not uri:
        raise RuntimeError("MONGODB_URI is not set")

    sentiment = result["sentiment"]
    workout = result["workout_plan"]
    diet = result["diet_plan"]
    created = datetime.now(timezone.utc)

    doc = {
        "text": raw_text,
        "display_name": display_name or "",
        "dominant_sentiment": sentiment["dominant"],
        "scores": sentiment["scores"],
        "confidence_pct": sentiment.get("confidence_pct"),
        "override_applied": sentiment.get("override_applied", False),
        "workout_mode": workout.get("mode", ""),
        "diet_mode": diet.get("mode", ""),
        "message": result.get("message", ""),
        "created_at": created,
        "author": AUTHORS,
    }

    db_name, coll_name = _db_names()
    doc_id = _run_isolated(_worker_insert, uri, db_name, coll_name, doc)
    doc["_id"] = doc_id
    doc["created_at"] = created.isoformat()
    return doc


def get_recent_history(limit: int = 20) -> list[dict[str, Any]]:
    uri = os.environ.get("MONGODB_URI", "").strip()
    if not uri:
        raise RuntimeError("MONGODB_URI is not set")
    db_name, coll_name = _db_names()
    return _run_isolated(_worker_fetch, uri, db_name, coll_name, limit)

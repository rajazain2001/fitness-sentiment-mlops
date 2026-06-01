"""MongoDB persistence for fitness sentiment analyses — Zain, Usama, Ali."""
import os
from datetime import datetime, timezone
from typing import Any

_client = None
_collection = None

AUTHORS = "Zain, Usama, Ali"


def is_db_configured() -> bool:
    return bool(os.getenv("MONGODB_URI", "").strip())


def _get_collection():
    global _client, _collection
    if _collection is not None:
        return _collection

    uri = os.environ.get("MONGODB_URI", "").strip()
    if not uri:
        raise RuntimeError("MONGODB_URI is not set")

    from pymongo import MongoClient

    db_name = os.getenv("MONGODB_DB_NAME", "fitness_app")
    coll_name = os.getenv("MONGODB_COLLECTION", "analyses")

    _client = MongoClient(
        uri,
        serverSelectionTimeoutMS=3000,
        connectTimeoutMS=3000,
        socketTimeoutMS=8000,
        waitQueueTimeoutMS=3000,
        maxPoolSize=5,
    )
    # Fail fast if Atlas is unreachable (avoids hanging the Gradio worker).
    _client.admin.command("ping")
    _collection = _client[db_name][coll_name]
    return _collection


def save_analysis(raw_text: str, result: dict, display_name: str | None = None) -> dict[str, Any]:
    """Persist one analysis; returns inserted document id as string."""
    sentiment = result["sentiment"]
    workout = result["workout_plan"]
    diet = result["diet_plan"]

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
        "created_at": datetime.now(timezone.utc),
        "author": AUTHORS,
    }

    coll = _get_collection()
    inserted = coll.insert_one(doc)
    doc["_id"] = str(inserted.inserted_id)
    doc["created_at"] = doc["created_at"].isoformat()
    return doc


def get_recent_history(limit: int = 20) -> list[dict[str, Any]]:
    coll = _get_collection()
    records = (
        coll.find()
        .sort("created_at", -1)
        .limit(limit)
        .max_time_ms(10000)
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
    return rows

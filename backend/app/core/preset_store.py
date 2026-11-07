from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from uuid import uuid4

TEMPLATE_LIBRARY = [
    {"key": "customer_update", "label": "Customer Update", "audience": "customer", "tone": "technical_commercial", "lengths": ["short", "medium"], "prompt_preset": "balanced"},
    {"key": "warm_prospect", "label": "Warm Prospect", "audience": "prospect", "tone": "warm_consultative", "lengths": ["short", "medium"], "prompt_preset": "direct"},
    {"key": "partner_note", "label": "Partner Note", "audience": "partner", "tone": "professional_neutral", "lengths": ["short", "medium"], "prompt_preset": "guarded"},
    {"key": "linkedin_post", "label": "LinkedIn Post", "audience": "linkedin_post", "tone": "social_light", "lengths": ["short"], "prompt_preset": "social"},
    {"key": "internal_summary", "label": "Internal Summary", "audience": "internal", "tone": "professional_neutral", "lengths": ["short", "medium"], "prompt_preset": "balanced"},
]

class PresetStore:
    def __init__(self, db_path: str | None = None) -> None:
        default_path = Path(__file__).resolve().parents[2] / "sales_copilot.db"
        self.db_path = str(db_path or default_path)
        self._init_db()

    def _connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS presets (
                    preset_id TEXT PRIMARY KEY,
                    label TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def list(self):
        with self._connect() as conn:
            rows = conn.execute("SELECT payload FROM presets ORDER BY updated_at DESC").fetchall()
            return [json.loads(r["payload"]) for r in rows]

    def save(self, payload: dict):
        preset_id = payload.get("key") or f"preset_{uuid4().hex[:8]}"
        template = next((t for t in TEMPLATE_LIBRARY if t["key"] == payload.get("template_key")), TEMPLATE_LIBRARY[0])
        record = {
            "key": preset_id,
            "label": payload.get("name") or template["label"],
            "template_key": template["key"],
            "audience": template["audience"],
            "tone": template["tone"],
            "lengths": template["lengths"],
            "prompt_preset": template["prompt_preset"],
            "template_version": "v1.0.0",
        }
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO presets(preset_id, label, payload)
                VALUES(?, ?, ?)
                ON CONFLICT(preset_id) DO UPDATE SET
                    label=excluded.label,
                    payload=excluded.payload,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (preset_id, record["label"], json.dumps(record, ensure_ascii=False)),
            )
            conn.commit()
        return record

preset_store = PresetStore()

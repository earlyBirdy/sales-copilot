from __future__ import annotations

import json
from pathlib import Path

from app.core.export_builder import build_crm_note, build_email_ready_block
from app.core.intake_pipeline import gmail_placeholder, normalize_unified_intake
from app.core.validators import validate_final_blocks

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"

def run_fixture(path: Path) -> dict:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload["kind"] == "unified_intake":
        source = normalize_unified_intake(payload["payload"])
        return {
            "fixture": payload["name"],
            "intake_mode": source["intake_mode"],
            "title_present": bool(source["title"]),
            "raw_text_present": bool(source["raw_text"]),
        }
    if payload["kind"] == "export_meta":
        session = payload["session"]
        blocks = validate_final_blocks(session["final_pack"]["final_editable_blocks"])
        return {
            "fixture": payload["name"],
            "crm_note_present": bool(build_crm_note(session)),
            "email_ready_present": bool(build_email_ready_block(session)),
            "block_count": len(blocks),
        }
    if payload["kind"] == "gmail_placeholder":
        result = gmail_placeholder(payload["payload"])
        return {
            "fixture": payload["name"],
            "status": result["status"],
        }
    raise ValueError(f"Unknown fixture kind: {payload['kind']}")

def main() -> None:
    results = []
    for path in sorted(FIXTURES_DIR.glob("*.json")):
        try:
            results.append(run_fixture(path))
        except Exception as exc:
            results.append({"fixture": path.name, "ok": False, "error": str(exc)})
    print(json.dumps({"results": results}, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

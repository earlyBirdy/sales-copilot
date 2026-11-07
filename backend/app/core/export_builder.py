from __future__ import annotations

def build_crm_note(session: dict) -> str:
    source = session.get("source", {})
    signals = session.get("sales_signals", {})
    points = signals.get("selling_points", [])[:3]
    return (
        f"Source: {source.get('title', 'Untitled')} | "
        f"Company: {source.get('sender_company', '') or signals.get('company', '')} | "
        f"Key points: {', '.join(points)}"
    )

def build_email_ready_block(session: dict) -> str:
    blocks = session.get("final_pack", {}).get("final_editable_blocks", [])
    if not blocks:
        return ""
    return blocks[0]["text"]

def build_markdown_bundle(session: dict) -> str:
    summary = session.get("final_pack", {}).get("source_summary", [])
    blocks = session.get("final_pack", {}).get("final_editable_blocks", [])
    crm_note = build_crm_note(session)
    email_ready = build_email_ready_block(session)

    lines = ["# Sales Copilot Export", "", "## Source Summary"]
    for item in summary:
        lines.append(f"- {item}")
    lines.extend(["", "## Copy-ready Blocks"])
    for block in blocks:
        lines.extend([f"### {block['label']}", block["text"], ""])
    lines.extend(["## CRM Note", crm_note, "", "## Email-ready Block", email_ready, ""])
    return "\n".join(lines)

from __future__ import annotations

from pathlib import Path


class PromptLoader:
    def __init__(self, prompts_dir: str | Path | None = None) -> None:
        default_dir = Path(__file__).resolve().parents[1] / "prompts"
        self.prompts_dir = Path(prompts_dir) if prompts_dir else default_dir

    def load(self, filename: str) -> str:
        path = self.prompts_dir / filename
        return path.read_text(encoding="utf-8").strip()

from pydantic import BaseModel, Field
from typing import List

class GenerateDraftsRequest(BaseModel):
    session_id: str
    audience: str
    tone: str
    lengths: List[str] = Field(min_length=1)
    prompt_preset: str = "balanced"

class SelectDraftRequest(BaseModel):
    draft_id: str

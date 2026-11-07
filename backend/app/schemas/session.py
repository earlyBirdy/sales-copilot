from pydantic import BaseModel, Field
from typing import Any, Dict, List, Optional

class RevisionHistoryItem(BaseModel):
    revision_id: str
    draft_id: str
    instruction: str
    result_text: str

class ApprovalUpdateRequest(BaseModel):
    approval_state: str

class EditableBlockUpdateRequest(BaseModel):
    label: str
    text: str = Field(min_length=1)

class SessionResponse(BaseModel):
    session_id: str
    status: str
    approval_state: str = "drafted"
    source: Dict[str, Any]
    normalized_source: Dict[str, Any]
    sales_signals: Dict[str, Any]
    draft_outputs: List[Dict[str, Any]]
    selected_draft_id: Optional[str] = None
    revision_history: List[RevisionHistoryItem]
    review_notes: List[str]
    final_pack: Dict[str, Any]

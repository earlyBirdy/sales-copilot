from pydantic import BaseModel
from typing import Optional

class ExportRequest(BaseModel):
    session_id: str
    draft_ids: Optional[list[str]] = None

from pydantic import BaseModel

class SafetyReviewRequest(BaseModel):
    session_id: str
    draft_id: str

from pydantic import BaseModel
class GuardrailRequest(BaseModel):
    session_id:str
    draft_id:str

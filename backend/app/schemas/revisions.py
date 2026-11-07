from pydantic import BaseModel, Field
class ReviseDraftRequest(BaseModel):
    session_id:str
    draft_id:str
    instruction:str=Field(min_length=1,max_length=3000)

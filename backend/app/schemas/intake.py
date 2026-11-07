from pydantic import BaseModel, Field

class UnifiedIntakeRequest(BaseModel):
    intake_mode: str = Field(min_length=1)
    source_type: str = Field(min_length=1)
    title: str = ""
    raw_text: str = ""
    url: str = ""
    sender_company: str = ""
    user_goal: str = ""
    upload_name: str = ""

class GmailPlaceholderRequest(BaseModel):
    title: str = ""
    sender_company: str = ""
    user_goal: str = ""

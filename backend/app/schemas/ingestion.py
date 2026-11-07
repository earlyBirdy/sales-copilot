from pydantic import BaseModel, Field

class ArticleFetchRequest(BaseModel):
    url: str = Field(min_length=1)
    title: str = ""
    user_goal: str = ""

class EmailCleanupRequest(BaseModel):
    raw_email_text: str = Field(min_length=1)
    title: str = ""
    sender_company: str = ""
    user_goal: str = ""

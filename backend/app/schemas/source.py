from pydantic import BaseModel, Field
class SourceAnalyzeRequest(BaseModel):
    source_type:str='email'
    title:str=''
    raw_text:str=Field(min_length=1)
    sender_company:str=''
    user_goal:str=''
    url:str=''

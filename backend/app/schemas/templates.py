from pydantic import BaseModel, Field

class SavedPresetRequest(BaseModel):
    name: str = Field(min_length=1)
    template_key: str = "customer_update"
    audience: str = "customer"
    tone: str = "technical_commercial"
    lengths: list[str] = ["short", "medium"]
    prompt_preset: str = "balanced"

class GenerateTemplateRequest(BaseModel):
    session_id: str
    template_key: str
    selected_cta: str = ""

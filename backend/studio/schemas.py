from pydantic import BaseModel, Field
from typing import List, Dict, Optional

class BriefIn(BaseModel):
    channel_id: str = Field(default="channel-a")
    template_id: str = Field(default="template-card3")
    topic: str
    bullets: List[str] = Field(default_factory=list)
    refs: List[str] = Field(default_factory=list)
    target_seconds: int = 45
    language: str = "ko"

class JobOut(BaseModel):
    job_id: str
    status: str
    output_mp4: Optional[str] = None
    eval: Optional[Dict] = None
    log: List[str] = Field(default_factory=list)

class FeedbackIn(BaseModel):
    verdict: str = Field(pattern="^(good|bad)$")
    issue_type: str = "script"  # script|tone|visual|subtitle|etc
    comment: str

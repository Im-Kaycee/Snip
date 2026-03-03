from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

class URLCreate(BaseModel):
    original_url: HttpUrl  # validates proper URL

class URLInfo(BaseModel):
    original_url: HttpUrl
    short_code: str
    short_url: str
    expires_at: Optional[datetime] = None
    click_count: int
    
class URLStats(BaseModel):
    short_code: str
    original_url: HttpUrl
    created_at: datetime
    expires_at: Optional[datetime] = None
    click_count: int
    
class URLMinimal(BaseModel):
    original_url: str
    #short_code: str
    short_url: str
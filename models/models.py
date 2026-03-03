from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional
from datetime import timezone
def now_utc():
    return datetime.now(timezone.utc)
class URL(SQLModel, table=True):
    """
    URL model for shortener
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    original_url: str = Field(index=True)
    short_code: Optional[str] = Field(default=None, index=True, unique=True)
    created_at: datetime = Field(default_factory=now_utc)
    expires_at: Optional[datetime] = None
    click_count: int = Field(default=0)
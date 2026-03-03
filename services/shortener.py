from datetime import datetime, timezone, timedelta
from sqlmodel import Session
from models.models import URL
from utils import encode_base62
from database.redis import r

def utc_now():
    return datetime.now(timezone.utc)


def create_short_url(session: Session, original_url: str, expires_at: datetime = None) -> URL:
    if expires_at is None:
        expires_at = utc_now() + timedelta(days=7)
    new_url = URL(original_url=original_url, expires_at=expires_at)
    session.add(new_url)
    session.commit()
    session.refresh(new_url)

    short_code = encode_base62(new_url.id)
    new_url.short_code = short_code
    session.add(new_url)
    session.commit()
    session.refresh(new_url)

    r.set(short_code, original_url, ex=7*24*3600)

    return new_url
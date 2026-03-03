from fastapi import APIRouter, FastAPI, Depends, HTTPException
from pydantic import HttpUrl
from sqlmodel import Session, select
from database.redis import r
from database.database import get_session
from services.shortener import create_short_url
from fastapi.responses import RedirectResponse
from sqlmodel import Session, select
from datetime import datetime, timedelta, timezone
from models.models import URL
from schemas.schemas import *
from fastapi import Request, HTTPException
import time

def utc_now():
    return datetime.now(timezone.utc)
router = APIRouter(prefix="/api", tags=["urls"])

def token_bucket_rate_limit(
    request: Request,
    max_tokens: int = 10,       # bucket capacity
    refill_rate: float = 1/6    # tokens per second (10 tokens/min)
):
    ip = request.client.host
    key = f"tokenbucket:{ip}"

    # Fetch current state
    data = r.get(key)
    now = time.time()

    if data:
        tokens_left, last_refill = map(float, data.split(":"))

        # Refill tokens based on time passed
        elapsed = now - last_refill
        tokens_left = min(max_tokens, tokens_left + elapsed * refill_rate)
    else:
        tokens_left = max_tokens
        last_refill = now

    if tokens_left >= 1:
        # Consume a token
        tokens_left -= 1
        r.set(key, f"{tokens_left}:{now}")
    else:
        # Bucket empty → rate limit exceeded
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
@router.post("/shorten", response_model=URLInfo)
def shorten_url(url_create: URLCreate, session: Session = Depends(get_session), request: Request = None):
    token_bucket_rate_limit(request, max_tokens=10, refill_rate=1/6)
    url_obj = create_short_url(session, str(url_create.original_url), expires_at=None)
    
    short_url = f"http://localhost:8000/api/{url_obj.short_code}"
    
    return URLInfo(
        original_url=url_obj.original_url,
        short_code=url_obj.short_code,
        short_url=short_url,
        expires_at=url_obj.expires_at,
        click_count=url_obj.click_count
    )
@router.get("/stats/{short_code}", response_model=URLStats)
def get_url_stats(short_code: str, session: Session = Depends(get_session)):
    statement = select(URL).where(URL.short_code == short_code)
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")
    short_url = f"http://localhost:8000/api/{result.short_code}"
    return URLStats(
        short_code=short_url,
        original_url=result.original_url,
        created_at=result.created_at,
        expires_at=result.expires_at,
        click_count=result.click_count
    )
    
@router.get("/urls", response_model=list[URLMinimal])
def get_urls(session: Session = Depends(get_session)):
    statement = select(URL)
    results = session.exec(statement).all()

    return [
    URLMinimal(
        original_url=url.original_url,
        #short_code=url.short_code,
        short_url=f"http://localhost:8000/api/{url.short_code}"
    )
    for url in results
]
@router.get("/{short_code}")
def redirect_url(short_code: str, session: Session = Depends(get_session)):
    statement = select(URL).where(URL.short_code == short_code)
    result = session.exec(statement).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Short URL not found")
    
   
    if result.expires_at:
        # ensure we compare timezone-aware datetimes (DB may return a naive object)
        expires = result.expires_at
        if expires.tzinfo is None:
            expires = expires.replace(tzinfo=timezone.utc)
        if expires < utc_now():
            raise HTTPException(status_code=410, detail="Short URL expired")
    
    
    result.click_count += 1
    session.add(result)
    session.commit()
    session.refresh(result)
    r.set(short_code, result.original_url, ex=7*24*3600)
    
   
    return RedirectResponse(url=result.original_url)


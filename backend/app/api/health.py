from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import logging

from app.config import settings
from app.models import HealthResponse
from app.database import get_db
from app.cache import redis_client

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    db_status = "healthy"
    try:
        db.execute("SELECT 1")
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        db_status = "unhealthy"
    
    redis_status = "healthy"
    if not redis_client.client:
        redis_status = "unhealthy"
    
    gemini_status = "healthy"
    if not settings.GEMINI_API_KEY:
        gemini_status = "unconfigured"
    
    return HealthResponse(
        status="healthy" if db_status == "healthy" and redis_status == "healthy" else "degraded",
        version=settings.APP_VERSION,
        database=db_status,
        redis=redis_status,
        gemini_api=gemini_status
    )
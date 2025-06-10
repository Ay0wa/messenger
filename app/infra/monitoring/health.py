from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.database import get_async_session
from app.infra.logging_setup.config import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get("/")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "messenger-api"}


@router.get("/detailed")
async def detailed_health_check(
    db: AsyncSession = Depends(get_async_session)
) -> Dict[str, Any]:
    health_status = {
        "status": "healthy",
        "service": "messenger-api",
        "checks": {}
    }
    
    try:
        result = await db.execute(text("SELECT 1"))
        result.scalar()
        health_status["checks"]["database"] = {"status": "healthy"}
        logger.info("Database health check passed")
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        logger.error("Database health check failed", error=str(e))
    
    # TODO: Добавить проверку Redis когда подключим
    # TODO: Добавить проверку других сервисов
    
    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)
    
    return health_status
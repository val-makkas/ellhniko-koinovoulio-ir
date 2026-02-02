from fastapi import APIRouter, Query
from app.core.data_loader import load_speeches

router = APIRouter()

@router.get("/")
async def speeches(limit: int = Query(10, ge=1, le=100)):
    return load_speeches(limit)
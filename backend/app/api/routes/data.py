from fastapi import APIRouter
from app.core.data_loader import load_sample

router = APIRouter()

@router.get("/sample")
async def sample():
    return load_sample(5)
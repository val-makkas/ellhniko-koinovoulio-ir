from fastapi import APIRouter
from pydantic import BaseModel
from app.core.text_cleaner import clean_text

router = APIRouter()

class CleanRequest(BaseModel):
    text: str

@router.post("/")
async def clean(request: CleanRequest):
    return {"cleaned": clean_text(request.text)}
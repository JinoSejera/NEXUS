from fastapi import APIRouter, Depends, HTTPException, Request, Query

from slowapi import Limiter
from slowapi.util import get_remote_address

from ....services.capstone_title_gen_service import CapstoneTitleService
from ....models.capstone_models import GeneratedTitles
from ....dependencies import get_capstone_title_service

router = APIRouter(prefix="/api/v1")
limiter = Limiter(key_func=get_remote_address)

@router.post("/generate_titles", response_model=GeneratedTitles)
@limiter.limit("5/minute")
async def generate_titles(
    request: Request,
    query: str = Query(..., description="query used to create titles"), 
    title_service: CapstoneTitleService = Depends(get_capstone_title_service)
):
    try:
        titles = await title_service.generate_capstone_titles(query)
        return titles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error encountered at: {e}")
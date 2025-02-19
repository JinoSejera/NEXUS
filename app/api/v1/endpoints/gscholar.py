from fastapi import APIRouter, Depends, Query, Request
from slowapi.util import get_remote_address
from slowapi import Limiter
from ....services.gscholar_service import GoogleScholarService
from ....models.gscholar_models import GScholarResponse
from ....dependencies import get_gscholar_service

router = APIRouter(prefix='/api/v1')
limiter = Limiter(key_func=get_remote_address)

@router.get("/search", response_model=GScholarResponse)
@limiter.limit("5/minute")
async def search_google_scholar(
    request: Request,
    query: str = Query(..., description="query to search in google scholar"),
    gscholar_service: GoogleScholarService = Depends(get_gscholar_service)
):
    response = await gscholar_service.search_rrls(query=query, number_of_rrl=3)
    
    return response
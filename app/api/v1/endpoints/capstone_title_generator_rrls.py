from fastapi import APIRouter, Depends, HTTPException, Request, Query

from slowapi import Limiter
from slowapi.util import get_remote_address

from ....services.capstone_title_gen_service import CapstoneTitleService
from ....services.gscholar_service import GoogleScholarService
from ....models.capstone_title_rrl_model import CapstoneTitlesWithRRL, GeneratedTitlesResponse
from ....dependencies import get_capstone_title_service, get_gscholar_service

from typing import List

router = APIRouter(prefix="/api/v1")
limiter = Limiter(key_func=get_remote_address)

@router.post('/generate_capstone_titles', response_model=GeneratedTitlesResponse)
@limiter.limit("3/hour")
async def generate_capstone_titles(
    request: Request,
    query: str = Query(..., description="query used to create titles"), 
    title_service: CapstoneTitleService = Depends(get_capstone_title_service),
    google_scholar_service: GoogleScholarService = Depends(get_gscholar_service)  
):
    
    try:
        titles = await title_service.generate_capstone_titles(query)

        titles_with_rrl:List[CapstoneTitlesWithRRL] = []
        
        for title in titles.results:
            if title.title:
                rrl_results = await google_scholar_service.search_rrls(query=title.title, number_of_rrl=3)
                titles_with_rrl.append(CapstoneTitlesWithRRL(application=title.application, title=title.title, rrls=rrl_results.results))
        
        return GeneratedTitlesResponse(generated_titles=titles_with_rrl)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate Capstone Titles due to error encountered: {e}")
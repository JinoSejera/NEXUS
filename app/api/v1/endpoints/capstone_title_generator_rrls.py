import logging
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request

from ....contract.gscholar_service_base import GScholarServiceBase
from ....contract.title_gen_service_base import TitleGenServiceBase
from ....models.capstone_title_rrl_model import CapstoneTitlesWithRRL, GeneratedTitlesResponse
from ....dependencies import get_capstone_title_service, get_gscholar_service
from ....models.request_body_model import RequestBody 
from ....utils.limiter import limiter

api = 'Capstone Title Generator with RRLs'
router = APIRouter(prefix="/api/v1/generate_title")
_logger = logging.getLogger(__name__)

@router.post('/generate', response_model=GeneratedTitlesResponse, tags=[api])
@limiter.limit("3/hour")
async def generate_capstone_titles(
    request: Request,
    request_body: RequestBody,
    title_service: TitleGenServiceBase = Depends(get_capstone_title_service),
    google_scholar_service: GScholarServiceBase = Depends(get_gscholar_service)  
): 
    try:
        
        titles = await title_service.generate_capstone_titles(request_body.query, request_body.course)

        titles_with_rrl:List[CapstoneTitlesWithRRL] = []
        
        for title in titles.results:
            _logger.info(f"Generating RRL for Title: {title.title}")
            if title.title:
                rrl_results = await google_scholar_service.search_rrls(query=title.title, number_of_rrl=3)
                _logger.info(f"RRLs for Title: {rrl_results.results}")
                titles_with_rrl.append(CapstoneTitlesWithRRL(application=title.application, overview=title.overview, title=title.title, rrls=rrl_results.results))
        
        return GeneratedTitlesResponse(generated_titles=titles_with_rrl)
    except Exception as e:
        _logger.error(f"Failed to generate Capstone Titles due to error encountered: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate Capstone Titles due to error encountered: {e}")

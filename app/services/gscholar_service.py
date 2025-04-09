from ..repos.gscholar_repository import GoogleScholarRepository
from ..models.gscholar_models import GScholarSearchResult, GScholarResponse
from typing import List
import logging

logger = logging.getLogger(__name__)

class GoogleScholarService:
    def __init__(self, repository: GoogleScholarRepository):
        self.__repository = repository
        
    async def search_rrls(self, query:str, number_of_rrl:int) -> GScholarResponse:
        try:
            results = await self.__repository.search_rrl(query, number_of_rrl)
            search_results:List[GScholarSearchResult] = [GScholarSearchResult(title=result['title'], link=result['link']) for result in results]
            
            return GScholarResponse(query=query, results=search_results)
        except Exception as e:
            logger.error(f"Failed to search for RRLs for title: '{query}', due to error encountered: {e}")
            raise e
        
    
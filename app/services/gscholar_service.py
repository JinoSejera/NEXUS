from typing import List
import logging

from ..contract.gscholar_service_base import GScholarServiceBase
from ..contract.gscholar_base import GScholarBase
from ..models.gscholar_models import GScholarSearchResult, GScholarResponse


logger = logging.getLogger(__name__)

class GoogleScholarService(GScholarServiceBase):
    __gscholar: "GScholarBase"
    
    def __init__(self, gscholar: "GScholarBase"):
        self.__gscholar = gscholar
        
    async def search_rrls(self, query:str, number_of_rrl:int) -> GScholarResponse:
        try:
            results = await self.__gscholar.search_rrl(query, number_of_rrl)
            logger.info(f"Successfully searched for RRLs for title: '{query}'\nResults: {results}")
            search_results:List[GScholarSearchResult] = [GScholarSearchResult(title=result['title'], link=result['link']) for result in results]
            
            return GScholarResponse(query=query, results=search_results)
        except Exception as e:
            logger.error(f"Failed to search for RRLs for title: '{query}', due to error encountered: {e}")
            raise e
        
    
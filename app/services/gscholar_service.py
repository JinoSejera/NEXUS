from ..repos.gscholar_repository import GoogleScholarRepository
from ..models.gscholar_models import GScholarSearchResult, GScholarResponse
from typing import List

class GoogleScholarService:
    def __init__(self, repository: GoogleScholarRepository):
        self.repository = repository
        
    async def search_rrls(self, query:str, number_of_rrl:int) -> GScholarResponse:
        results = await self.repository.search_rrl(query, number_of_rrl)
        search_results:List[GScholarSearchResult] = [GScholarSearchResult(title=result['title'], link=result['link']) for result in results]
        
        return GScholarResponse(query=query, results=search_results)
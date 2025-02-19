from ..repos.title_generator_repository import CapstoneTitleGeneratorRepository
from ..models.capstone_models import GeneratedTitles, GeneratedTitle

from typing import List

class CapstoneTitleService:
    def __init__(self, repository: CapstoneTitleGeneratorRepository):
        self._repository = repository
        
    
    async def generate_capstone_titles(self, query:str) -> GeneratedTitles:
        
        results = await self._repository.generate_titles(query)
        
        titles:List[GeneratedTitle] = [GeneratedTitle(application=result['application'], title=result['title']) for result in results['generated_titles']]
        
        return GeneratedTitles(results=titles)
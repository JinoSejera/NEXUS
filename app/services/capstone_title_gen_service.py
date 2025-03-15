from ..repos.title_generator_repository import CapstoneTitleGeneratorRepository
from ..models.capstone_models import GeneratedTitles, GeneratedTitle

from typing import List
import logging

logger = logging.getLogger(__name__)


class CapstoneTitleService:
    def __init__(self, repository: CapstoneTitleGeneratorRepository):
        self._repository = repository
        
    
    async def generate_capstone_titles(self, query:str) -> GeneratedTitles:
        try:
            results = await self._repository.generate_titles(query)
            
            titles:List[GeneratedTitle] = [GeneratedTitle(application=result['application'], title=result['title']) for result in results['generated_titles']]
            
            return GeneratedTitles(results=titles)
        except Exception as e:
            logger.error(f"Failed to generate Capstone Titles for '{query}', due to error encountered: {e}")
            raise e
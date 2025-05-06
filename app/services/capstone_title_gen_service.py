from typing import List
import logging

from ..contract.title_gen_service_base import TitleGenServiceBase
from ..models.capstone_models import GeneratedTitles, GeneratedTitle
from ..contract.title_gen_base import TitleGenBase

logger = logging.getLogger(__name__)


class CapstoneTitleService(TitleGenServiceBase):
    __title_gen: "TitleGenBase"
    def __init__(self, title_gen: "TitleGenBase"):
        self.__title_gen = title_gen
        
    
    async def generate_capstone_titles(self, query:str, course:str) -> GeneratedTitles:
        try:
            results = await self.__title_gen.generate_titles(query, course)
            
            titles:List[GeneratedTitle] = [GeneratedTitle(application=result['application'], 
                                                          title=result['title'], 
                                                          overview=result['overview']) for result in results['generated_titles']
                                           ]
            
            return GeneratedTitles(results=titles)
        except Exception as e:
            logger.error(f"Failed to generate Capstone Titles for '{query}', due to error encountered: {e}")
            raise e
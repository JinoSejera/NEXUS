from abc import ABC, abstractmethod

from ..models.capstone_models import GeneratedTitles

class TitleGenServiceBase(ABC):

    @abstractmethod
    async def generate_capstone_titles(self, query:str, course:str) -> GeneratedTitles:
        """_summary_

        Args:
            query (str): _description_
            course (str): _description_

        Returns:
            GeneratedTitles: _description_
        """
        pass
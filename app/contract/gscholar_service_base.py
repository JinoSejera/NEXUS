from abc import ABC, abstractmethod

from ..models.gscholar_models import GScholarResponse

class GScholarServiceBase(ABC):
    """
    Abstract base class for Google Scholar service.
    """

    @abstractmethod
    async def search_rrls(self, query:str, number_of_rrl:int) -> GScholarResponse:
        """
        Search Google Scholar for a given query and return a list of results.
        """
        pass
from typing import List, Dict
from abc import ABC, abstractmethod

class GScholarBase(ABC):
    
    @abstractmethod
    async def search_rrl(query: str, rrl_count:int) -> List[Dict[str, str]]:
        """
        Search Google Scholar for a given query and return a list of results.
        """
        pass
    
    
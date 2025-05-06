from abc import ABC, abstractmethod
from typing import Dict, Any

class TitleGenBase(ABC):
    """
    Abstract base class for title generation.
    """
    
    @abstractmethod
    async def generate_titles(self, query: str, course:str) -> Dict[str, Any]:
        """
        Generate a title based on the provided prompt.
        """
        pass
    
from pydantic import BaseModel
from typing import List

class GScholarSearchResult(BaseModel):
    title:str
    link:str
    
class GScholarResponse(BaseModel):
    query: str
    results: List[GScholarSearchResult]
    
    
from pydantic import BaseModel
from typing import List
from .gscholar_models import GScholarSearchResult
    
class CapstoneTitlesWithRRL(BaseModel):
    application:str
    title:str
    overview:str
    rrls: List[GScholarSearchResult]

class GeneratedTitlesResponse(BaseModel):
    generated_titles: List[CapstoneTitlesWithRRL]
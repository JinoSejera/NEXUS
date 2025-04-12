from pydantic import BaseModel
from typing import List

class GeneratedTitle(BaseModel):
    overview:str
    application:str
    title:str
    
class GeneratedTitles(BaseModel):
    results: List[GeneratedTitle]
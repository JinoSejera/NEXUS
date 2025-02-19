from pydantic import BaseModel
from typing import List

class GeneratedTitle(BaseModel):
    application:str
    title:str
    
class GeneratedTitles(BaseModel):
    results: List[GeneratedTitle]
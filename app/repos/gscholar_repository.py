
import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
from typing import List, Dict

from ..contract.gscholar_base import GScholarBase
import logging

logger = logging.getLogger(__name__)

class GoogleScholarRepository(GScholarBase):
    @staticmethod
    async def search_rrl(query: str, rrl_number: int) -> List[Dict[str, str]]:
        uri = f"https://scholar.google.com/scholar?q={query}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(uri, headers=headers) as response:
                    response.raise_for_status()
                    
                    text = await response.text()
                    
                    soup = BeautifulSoup(text, 'html.parser')
                    result = []
                    for item in soup.find_all('div', class_='gs_ri'):
                        title_tag = item.find('h3', class_='gs_rt')
                        if title_tag:
                            link_tag = title_tag.find('a')
                            title = title_tag.text
                            link = link_tag['href'] if link_tag else None
                            result.append({
                                "title": title,
                                "link": link
                            })
                    logger.info(f"Successfully fetched {len(result)} results for query: '{query}'\nResults: {result}")
                    return result[:rrl_number]
            except aiohttp.ClientError as e:
                raise HTTPException(status_code=500,
                                    detail=f"HTTP error while fetching data from Google Scholar: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Unexpected error: {str(e)}")
            finally:
                await session.close()
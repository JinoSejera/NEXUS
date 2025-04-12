import aiohttp
from bs4 import BeautifulSoup
from fastapi import HTTPException
from typing import List, Dict

class GoogleScholarRepository:
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
                        link_tag = item.find('a')
                        
                        if title_tag and link_tag:
                            title = title_tag.text
                            link = link_tag['href']
                            result.append({
                                "title": title,
                                "link": link
                            })
                    
                    return result[:rrl_number]
            except aiohttp.ClientError as e:
                raise HTTPException(status_code=500,
                                    detail=f"HTTP error while fetching data from Google Scholar: {str(e)}")
            except Exception as e:
                raise HTTPException(status_code=500,
                                    detail=f"Unexpected error: {str(e)}")
            finally:
                await session.close()
from typing import List, Dict, Optional
import httpx
from app.core.config import settings

class SearchService:
    def __init__(self):
        self.api_key = settings.TAVILY_API_KEY
        self.enabled = settings.ENABLE_WEB_SEARCH and self.api_key
    
    async def search(self, query: str, max_results: int = 5) -> List[Dict]:
        """
        Search the web using Tavily API
        """
        if not self.enabled:
            return []
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.tavily.com/search",
                    json={
                        "api_key": self.api_key,
                        "query": query,
                        "max_results": max_results
                    },
                    timeout=10.0
                )
                
                if response.status_code == 200:
                    data = response.json()
                    return data.get("results", [])
        except Exception as e:
            print(f"Search error: {e}")
        
        return []
    
    def format_sources(self, results: List[Dict]) -> str:
        """
        Format search results for injection into prompt
        """
        if not results:
            return ""
        
        formatted = "\n\nRelevant information from web search:\n"
        for i, result in enumerate(results, 1):
            formatted += f"\n[{i}] {result.get('title', 'Source')}\n"
            formatted += f"URL: {result.get('url', 'N/A')}\n"
            formatted += f"{result.get('content', '')}\n"
        
        return formatted

# Global search service instance
search_service = SearchService()
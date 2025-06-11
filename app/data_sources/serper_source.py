"""
Search-based data source using Serper API.
"""
import os
from typing import Dict, Any
import httpx

from app.data_sources.base_source import BaseDataSource


class SerperDataSource(BaseDataSource):
    """Data source for web search using Serper API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Serper data source.

        Args:
            api_key: Serper API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("SERPER_API_KEY")
        if not self.api_key:
            raise ValueError("Serper API key is required")

        self.base_url = "https://google.serper.dev/search"
        self.headers = {
            "X-API-KEY": self.api_key,
            "Content-Type": "application/json"
        }

    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Fetch search results for a company.

        Args:
            company_name: The name of the company
            url: The company's URL

        Returns:
            Dict containing search results
        """
        search_queries = [
            f"{company_name} company overview",
            f"{company_name} business model",
            f"{company_name} products services",
            f"{company_name} market size",
            f"{company_name} competitors",
            f"{company_name} revenue financial metrics",
            f"{company_name} funding investment rounds",
            f"{company_name} team executives management"
        ]

        results = {}
        async with httpx.AsyncClient() as client:
            for query in search_queries:
                payload = {
                    "q": query,
                    "num": 10
                }
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()

                # Store results by query type
                query_type = query.replace(f"{company_name} ", "")
                results[query_type] = response.json()

        return results

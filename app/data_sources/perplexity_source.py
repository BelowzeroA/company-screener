"""
Research-based data source using Perplexity API.
"""
import os
from typing import Dict, Any
import httpx

from app.data_sources.base_source import BaseDataSource


class PerplexityDataSource(BaseDataSource):
    """Data source for research using Perplexity API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Perplexity data source.

        Args:
            api_key: Perplexity API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("PERPLEXITY_API_KEY")
        if not self.api_key:
            raise ValueError("Perplexity API key is required")

        self.base_url = "https://api.perplexity.ai/search"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Fetch research data about a company.

        Args:
            company_name: The name of the company
            url: The company's URL

        Returns:
            Dict containing research data
        """
        research_queries = [
            f"Detailed analysis of {company_name}'s business model and products",
            f"{company_name} market size, TAM, and growth potential",
            f"{company_name} competitors and competitive landscape",
            f"{company_name} financial performance and key metrics",
            f"{company_name} funding history and investors",
            f"{company_name} leadership team background and experience"
        ]

        results = {}
        async with httpx.AsyncClient() as client:
            for query in research_queries:
                payload = {
                    "query": query,
                    "focus": "search"
                }
                response = await client.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                )
                response.raise_for_status()

                # Extract category from query and store results
                if "business model" in query:
                    category = "business_model"
                elif "market" in query:
                    category = "market_analysis"
                elif "competitors" in query:
                    category = "competitive_landscape"
                elif "financial" in query:
                    category = "financial_metrics"
                elif "funding" in query:
                    category = "fundraising"
                elif "leadership" in query:
                    category = "team"
                else:
                    category = "general"

                results[category] = response.json()

        return results

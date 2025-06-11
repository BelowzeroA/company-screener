"""
Funding data source via Tracxn API.
"""
import os
from typing import Dict, Any, List
import httpx

from app.data_sources.base_source import BaseDataSource


class TracxnDataSource(BaseDataSource):
    """Data source for funding and investor information via Tracxn API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the Tracxn data source.

        Args:
            api_key: Tracxn API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("TRACXN_API_KEY")
        if not self.api_key:
            raise ValueError("Tracxn API key is required")

        self.base_url = "https://platform.tracxn.com/api/2.0"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Fetch funding and investor data for a company.

        Args:
            company_name: The name of the company
            url: The company's URL

        Returns:
            Dict containing funding rounds and investor information
        """
        results = {
            "company_info": {},
            "funding_rounds": [],
            "investors": []
        }

        async with httpx.AsyncClient() as client:
            # Search for the company
            search_url = f"{self.base_url}/companies/search"
            search_payload = {
                "query": company_name,
                "limit": 5  # Get top 5 matches to ensure we find the right one
            }

            try:
                response = await client.post(
                    search_url,
                    headers=self.headers,
                    json=search_payload
                )
                response.raise_for_status()
                search_results = response.json()

                company_id = None
                domain = url.replace("https://", "").replace("http://", "").split("/")[0]

                # Try to find exact match by domain
                for company in search_results.get("companies", []):
                    if company.get("domain") == domain:
                        company_id = company.get("id")
                        results["company_info"] = company
                        break

                # If no match by domain, use the first result
                if not company_id and search_results.get("companies"):
                    company_id = search_results["companies"][0]["id"]
                    results["company_info"] = search_results["companies"][0]

                if not company_id:
                    return results

                # Get company funding rounds
                funding_url = f"{self.base_url}/companies/{company_id}/funding_rounds"
                funding_response = await client.get(funding_url, headers=self.headers)
                funding_response.raise_for_status()
                results["funding_rounds"] = funding_response.json().get("fundingRounds", [])

                # Get company investors
                investors_url = f"{self.base_url}/companies/{company_id}/investors"
                investors_response = await client.get(investors_url, headers=self.headers)
                investors_response.raise_for_status()
                results["investors"] = investors_response.json().get("investors", [])

                # Get detailed company information
                details_url = f"{self.base_url}/companies/{company_id}"
                details_response = await client.get(details_url, headers=self.headers)
                details_response.raise_for_status()
                results["company_details"] = details_response.json()

            except httpx.HTTPStatusError as e:
                results["error"] = {
                    "status_code": e.response.status_code,
                    "message": str(e)
                }

        return results

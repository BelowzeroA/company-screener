"""
LinkedIn data source using CoreSignal API.
"""
import os
from typing import Dict, Any
import httpx

from app.data_sources.base_source import BaseDataSource


class CoreSignalSource(BaseDataSource):
    """Data source for LinkedIn data via CoreSignal API."""

    def __init__(self, api_key: str = None):
        """
        Initialize the CoreSignal data source.

        Args:
            api_key: CoreSignal API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("CORESIGNAL_API_KEY")
        if not self.api_key:
            raise ValueError("CoreSignal API key is required")

        self.base_url = "https://api.coresignal.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Fetch LinkedIn data for a company.

        Args:
            company_name: The name of the company
            url: The company's URL

        Returns:
            Dict containing LinkedIn company and employee data
        """
        results = {
            "company_profile": {},
            "employees": []
        }

        async with httpx.AsyncClient() as client:
            # Search for the company profile
            search_url = f"{self.base_url}/linkedin/company/search"
            search_payload = {
                "query": company_name,
                "limit": 1  # Just the top match
            }

            try:
                response = await client.post(
                    search_url,
                    headers=self.headers,
                    json=search_payload
                )
                response.raise_for_status()
                search_results = response.json()

                if not search_results.get("results"):
                    return results

                company_id = search_results["results"][0]["id"]

                # Get detailed company information
                company_url = f"{self.base_url}/linkedin/company/{company_id}"
                company_response = await client.get(company_url, headers=self.headers)
                company_response.raise_for_status()
                results["company_profile"] = company_response.json()

                # Get key employees (executives, managers)
                employees_url = f"{self.base_url}/linkedin/company/{company_id}/employees"
                employees_payload = {
                    "limit": 20,
                    "filters": {
                        "position_title": {
                            "contains_any": ["CEO", "CTO", "CFO", "COO", "Chief",
                                           "Director", "VP", "Head", "President",
                                           "Founder", "Co-founder"]
                        }
                    }
                }

                employees_response = await client.post(
                    employees_url,
                    headers=self.headers,
                    json=employees_payload
                )
                employees_response.raise_for_status()
                results["employees"] = employees_response.json().get("results", [])

                # For key employees, get their detailed profiles
                for i, employee in enumerate(results["employees"]):
                    if i >= 10:  # Limit to top 10 employees to avoid API overuse
                        break

                    employee_id = employee["id"]
                    profile_url = f"{self.base_url}/linkedin/person/{employee_id}"

                    try:
                        profile_response = await client.get(
                            profile_url,
                            headers=self.headers
                        )
                        profile_response.raise_for_status()
                        results["employees"][i]["detailed_profile"] = profile_response.json()
                    except httpx.HTTPStatusError:
                        results["employees"][i]["detailed_profile"] = None

            except httpx.HTTPStatusError as e:
                results["error"] = {
                    "status_code": e.response.status_code,
                    "message": str(e)
                }

        return results

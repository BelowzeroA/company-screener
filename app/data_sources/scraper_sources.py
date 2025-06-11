"""
Web scraping data sources (ScraperAPI).
"""
import os
import re
from typing import Dict, Any, List
import httpx
from urllib.parse import urlparse, urljoin

from app.data_sources.base_source import BaseDataSource


class ScraperAPIDataSource(BaseDataSource):
    """Data source for scraping company websites using ScraperAPI."""

    def __init__(self, api_key: str = None):
        """
        Initialize the ScraperAPI data source.

        Args:
            api_key: ScraperAPI key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("SCRAPER_API_KEY")
        if not self.api_key:
            raise ValueError("ScraperAPI key is required")

        self.base_url = "http://api.scraperapi.com"

    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Scrape key pages from a company website.

        Args:
            company_name: The name of the company
            url: The company's URL

        Returns:
            Dict containing scraped content from key company pages
        """
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Common paths for important company pages
        target_paths = {
            "home": "/",
            "about": "/about",
            "about-us": "/about-us",
            "team": "/team",
            "our-team": "/our-team",
            "leadership": "/leadership",
            "products": "/products",
            "solutions": "/solutions",
            "services": "/services",
            "careers": "/careers"
        }

        results = {}
        async with httpx.AsyncClient() as client:
            for page_type, path in target_paths.items():
                full_url = urljoin(base_url, path)
                params = {
                    "api_key": self.api_key,
                    "url": full_url,
                    "render": "true"  # Enable JavaScript rendering
                }

                try:
                    response = await client.get(self.base_url, params=params)
                    response.raise_for_status()
                    results[page_type] = {
                        "url": full_url,
                        "html": response.text
                    }
                except httpx.HTTPStatusError as e:
                    if e.response.status_code == 404:
                        # Page not found, this is normal for some paths
                        continue
                    else:
                        # For other errors, add error info but continue
                        results[f"{page_type}_error"] = {
                            "url": full_url,
                            "status_code": e.response.status_code,
                            "error": str(e)
                        }

        # Extract key information from HTML content using basic patterns
        # In a real implementation, more sophisticated HTML parsing would be used
        cleaned_results = self._extract_key_info_from_html(results)

        return cleaned_results

    def _extract_key_info_from_html(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract key information from raw HTML content.

        Args:
            raw_results: Dictionary containing raw HTML content by page type

        Returns:
            Dictionary with extracted key information
        """
        cleaned_data = {}

        for page_type, data in raw_results.items():
            if "error" in page_type or "html" not in data:
                continue

            html = data["html"]

            # Extract text content (very basic implementation)
            # In production, use proper HTML parsing with BeautifulSoup or similar

            # Remove script and style elements
            html_no_scripts = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)
            html_no_styles = re.sub(r'<style.*?</style>', '', html_no_scripts, flags=re.DOTALL)

            # Extract text from HTML (very basic approach)
            text = re.sub(r'<[^>]+>', ' ', html_no_styles)

            # Clean up whitespace
            text = re.sub(r'\s+', ' ', text).strip()

            cleaned_data[page_type] = {
                "url": data["url"],
                "text_content": text
            }

        return cleaned_data

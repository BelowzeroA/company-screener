"""
Base data source interface for Company Screener.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseDataSource(ABC):
    """Base interface for all data sources."""

    @abstractmethod
    async def fetch_data(self, company_name: str, url: str) -> Dict[str, Any]:
        """
        Fetch data from the source.

        Args:
            company_name: Company name
            url: Company URL

        Returns:
            Dictionary containing the fetched data
        """
        pass

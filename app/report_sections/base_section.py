"""
Base class for all report sections.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseReportSection(ABC):
    """Base interface for all report sections."""

    @abstractmethod
    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the content for this report section.

        Args:
            raw_data: Combined raw data from all data sources

        Returns:
            Markdown formatted content for this section
        """
        pass

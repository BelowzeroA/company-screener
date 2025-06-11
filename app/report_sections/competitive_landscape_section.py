"""
Competitive Landscape report section.
"""
from typing import Dict, Any
import json

from app.report_sections.base_section import BaseReportSection
from app.aggregators.llm_aggregator import LLMAggregator


class CompetitiveLandscapeSection(BaseReportSection):
    """Section for competitive landscape analysis."""

    def __init__(self, llm_aggregator: LLMAggregator):
        """
        Initialize the competitive landscape section.

        Args:
            llm_aggregator: LLM aggregator for text generation
        """
        self.llm_aggregator = llm_aggregator

    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the competitive landscape section.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Markdown formatted competitive landscape analysis
        """
        system_prompt = """You are a competitive intelligence analyst creating a competitive landscape section for a company report.
        Identify direct competitors and their metrics (valuation, revenue, customers, geographic presence).
        Include indirect competitors if relevant.
        Create a table of competitors and provide a brief description of market saturation.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a competitive landscape section for {raw_data["company_name"]}.
        
        Company URL: {raw_data["url"]}
        
        Research Data: {json.dumps(raw_data.get("research_data", {}).get("competitive_landscape", {}), indent=2)}
        
        Search Data: {json.dumps(raw_data.get("search_data", {}).get("competitors", {}), indent=2)}
        
        Company Details: {json.dumps(raw_data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self.llm_aggregator.generate_content(prompt, system_prompt)

"""
Market Analysis report section.
"""
from typing import Dict, Any
import json

from app.report_sections.base_section import BaseReportSection
from app.aggregators.llm_aggregator import LLMAggregator


class MarketAnalysisSection(BaseReportSection):
    """Section for market analysis."""

    def __init__(self, llm_aggregator: LLMAggregator):
        """
        Initialize the market analysis section.

        Args:
            llm_aggregator: LLM aggregator for text generation
        """
        self.llm_aggregator = llm_aggregator

    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the market analysis section.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Markdown formatted market analysis
        """
        system_prompt = """You are a market analyst creating a market analysis section for a company report.
        Identify the Total Addressable Market (TAM), market segments, CAGR (Compound Annual Growth Rate), and geographic expansion.
        If exact figures are not available, provide reasonable estimates based on the industry and similar companies.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a market analysis section for {raw_data["company_name"]}.
        
        Company URL: {raw_data["url"]}
        
        Research Data: {json.dumps(raw_data.get("research_data", {}).get("market_analysis", {}), indent=2)}
        
        Search Data: {json.dumps(raw_data.get("search_data", {}).get("market size", {}), indent=2)}
        
        Company Details: {json.dumps(raw_data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self.llm_aggregator.generate_content(prompt, system_prompt)

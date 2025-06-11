"""
Financial Metrics report section.
"""
from typing import Dict, Any
import json

from app.report_sections.base_section import BaseReportSection
from app.aggregators.llm_aggregator import LLMAggregator


class FinancialMetricsSection(BaseReportSection):
    """Section for financial metrics analysis."""

    def __init__(self, llm_aggregator: LLMAggregator):
        """
        Initialize the financial metrics section.

        Args:
            llm_aggregator: LLM aggregator for text generation
        """
        self.llm_aggregator = llm_aggregator

    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the financial metrics section.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Markdown formatted financial metrics analysis
        """
        system_prompt = """You are a financial analyst creating a financial metrics section for a company report.
        Extract key metrics such as Revenue, EBITDA, GMV, MRR/ARR, and number of customers.
        If specific figures are not available, provide estimates based on available data or industry benchmarks.
        Format your response in Markdown with a table of metrics if possible."""

        prompt = f"""Based on the following data, create a financial metrics section for {raw_data["company_name"]}.
        
        Company URL: {raw_data["url"]}
        
        Research Data: {json.dumps(raw_data.get("research_data", {}).get("financial_metrics", {}), indent=2)}
        
        Search Data: {json.dumps(raw_data.get("search_data", {}).get("revenue financial metrics", {}), indent=2)}
        
        Company Details: {json.dumps(raw_data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self.llm_aggregator.generate_content(prompt, system_prompt)

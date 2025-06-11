"""
Company Overview report section.
"""
from typing import Dict, Any
import json

from app.report_sections.base_section import BaseReportSection
from app.aggregators.llm_aggregator import LLMAggregator


class CompanyOverviewSection(BaseReportSection):
    """Section for company overview."""

    def __init__(self, llm_aggregator: LLMAggregator):
        """
        Initialize the company overview section.

        Args:
            llm_aggregator: LLM aggregator for text generation
        """
        self.llm_aggregator = llm_aggregator

    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the company overview section.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Markdown formatted company overview
        """
        system_prompt = """You are a financial analyst creating a company overview section for a report.
        Write a concise but informative company overview in 4-6 lines.
        Include the company's business model, geography, stage, and uniqueness.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a company overview section for {raw_data["company_name"]}.
        
        Company URL: {raw_data["url"]}
        
        Website Data: {json.dumps(raw_data.get("website_data", {}).get("home", {}), indent=2)}
        
        About Page: {json.dumps(raw_data.get("website_data", {}).get("about", {}), indent=2)}
        
        LinkedIn Data: {json.dumps(raw_data.get("linkedin_data", {}).get("company_profile", {}), indent=2)}
        
        Search Data: {json.dumps(raw_data.get("search_data", {}).get("company overview", {}), indent=2)}
        """

        return await self.llm_aggregator.generate_content(prompt, system_prompt)

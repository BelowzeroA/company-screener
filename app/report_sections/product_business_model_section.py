"""
Product & Business Model report section.
"""
from typing import Dict, Any
import json

from app.report_sections.base_section import BaseReportSection
from app.aggregators.llm_aggregator import LLMAggregator


class ProductBusinessModelSection(BaseReportSection):
    """Section for product and business model."""

    def __init__(self, llm_aggregator: LLMAggregator):
        """
        Initialize the product and business model section.

        Args:
            llm_aggregator: LLM aggregator for text generation
        """
        self.llm_aggregator = llm_aggregator

    async def generate(self, raw_data: Dict[str, Any]) -> str:
        """
        Generate the product and business model section.

        Args:
            raw_data: Combined raw data from all sources

        Returns:
            Markdown formatted product and business model description
        """
        system_prompt = """You are a business analyst creating a product and business model section for a company report.
        Provide detailed information about the company's products, services, revenue streams and key characteristics.
        Present the information in a tabular or text form depending on the company type (consumer goods, SaaS, e-commerce, etc.).
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a detailed product and business model section for {raw_data["company_name"]}.
        
        Company URL: {raw_data["url"]}
        
        Website Data: 
        - Home: {json.dumps(raw_data.get("website_data", {}).get("home", {}), indent=2)}
        - Products: {json.dumps(raw_data.get("website_data", {}).get("products", {}), indent=2)}
        - Services: {json.dumps(raw_data.get("website_data", {}).get("services", {}), indent=2)}
        - Solutions: {json.dumps(raw_data.get("website_data", {}).get("solutions", {}), indent=2)}
        
        LinkedIn Data: {json.dumps(raw_data.get("linkedin_data", {}).get("company_profile", {}), indent=2)}
        
        Search Data: {json.dumps(raw_data.get("search_data", {}).get("products services", {}), indent=2)}
        
        Research Data: {json.dumps(raw_data.get("research_data", {}).get("business_model", {}), indent=2)}
        """

        return await self.llm_aggregator.generate_content(prompt, system_prompt)

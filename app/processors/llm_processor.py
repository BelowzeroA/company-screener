"""
LLM processing with GPT-4o for generating structured report sections.
"""
import os
from typing import Dict, Any
import json
import httpx

class LLMProcessor:
    """Class for processing data using LLMs (GPT-4o)."""

    def __init__(self, api_key: str = None):
        """
        Initialize the LLM processor.

        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required for the LLM processor")

        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = "gpt-4o"

    async def _call_llm(self, prompt: str, system_prompt: str = None) -> str:
        """
        Call the OpenAI API with a prompt.

        Args:
            prompt: User prompt to send to the API
            system_prompt: Optional system prompt to provide context

        Returns:
            Generated text response
        """
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            return result["choices"][0]["message"]["content"]

    async def generate_company_overview(self, data: Dict[str, Any]) -> str:
        """
        Generate the company overview section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted company overview
        """
        system_prompt = """You are a financial analyst creating a company overview section for a report.
        Write a concise but informative company overview in 4-6 lines.
        Include the company's business model, geography, stage, and uniqueness.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a company overview section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Website Data: {json.dumps(data.get("website_data", {}).get("home", {}), indent=2)}
        
        About Page: {json.dumps(data.get("website_data", {}).get("about", {}), indent=2)}
        
        LinkedIn Data: {json.dumps(data.get("linkedin_data", {}).get("company_profile", {}), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("company overview", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_product_business_model(self, data: Dict[str, Any]) -> str:
        """
        Generate the product and business model section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted product and business model description
        """
        system_prompt = """You are a business analyst creating a product and business model section for a company report.
        Provide detailed information about the company's products, services, revenue streams and key characteristics.
        Present the information in a tabular or text form depending on the company type (consumer goods, SaaS, e-commerce, etc.).
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a detailed product and business model section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Website Data: 
        - Home: {json.dumps(data.get("website_data", {}).get("home", {}), indent=2)}
        - Products: {json.dumps(data.get("website_data", {}).get("products", {}), indent=2)}
        - Services: {json.dumps(data.get("website_data", {}).get("services", {}), indent=2)}
        - Solutions: {json.dumps(data.get("website_data", {}).get("solutions", {}), indent=2)}
        
        LinkedIn Data: {json.dumps(data.get("linkedin_data", {}).get("company_profile", {}), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("products services", {}), indent=2)}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("business_model", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_market_analysis(self, data: Dict[str, Any]) -> str:
        """
        Generate the market analysis section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted market analysis
        """
        system_prompt = """You are a market analyst creating a market analysis section for a company report.
        Identify the Total Addressable Market (TAM), market segments, CAGR (Compound Annual Growth Rate), and geographic expansion.
        If exact figures are not available, provide reasonable estimates based on the industry and similar companies.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a market analysis section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("market_analysis", {}), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("market size", {}), indent=2)}
        
        Company Details: {json.dumps(data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_competitive_landscape(self, data: Dict[str, Any]) -> str:
        """
        Generate the competitive landscape section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted competitive landscape analysis
        """
        system_prompt = """You are a competitive intelligence analyst creating a competitive landscape section for a company report.
        Identify direct competitors and their metrics (valuation, revenue, customers, geographic presence).
        Include indirect competitors if relevant.
        Create a table of competitors and provide a brief description of market saturation.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a competitive landscape section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("competitive_landscape", {}), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("competitors", {}), indent=2)}
        
        Company Details: {json.dumps(data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_financial_metrics(self, data: Dict[str, Any]) -> str:
        """
        Generate the financial metrics section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted financial metrics analysis
        """
        system_prompt = """You are a financial analyst creating a financial metrics section for a company report.
        Extract key metrics such as Revenue, EBITDA, GMV, MRR/ARR, and number of customers.
        If specific figures are not available, provide estimates based on available data or industry benchmarks.
        Format your response in Markdown with a table of metrics if possible."""

        prompt = f"""Based on the following data, create a financial metrics section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("financial_metrics", {}), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("revenue financial metrics", {}), indent=2)}
        
        Company Details: {json.dumps(data.get("funding_data", {}).get("company_details", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_fundraising_history(self, data: Dict[str, Any]) -> str:
        """
        Generate the fundraising history section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted fundraising history
        """
        system_prompt = """You are a venture capital analyst creating a fundraising history section for a company report.
        List funding rounds with dates, investment amounts, and company valuations.
        Format as a chronological table with the most recent rounds first.
        Format your response in Markdown."""

        prompt = f"""Based on the following data, create a fundraising history section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        Funding Data: 
        - Rounds: {json.dumps(data.get("funding_data", {}).get("funding_rounds", []), indent=2)}
        - Investors: {json.dumps(data.get("funding_data", {}).get("investors", []), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("funding investment rounds", {}), indent=2)}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("fundraising", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

    async def generate_team_stakeholders(self, data: Dict[str, Any]) -> str:
        """
        Generate the team and key stakeholders section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted team and stakeholders analysis
        """
        system_prompt = """You are an organizational analyst creating a team and key stakeholders section for a company report.
        List key employees and investors with their roles and experience.
        Evaluate the relevance of their experience and achievements.
        Format your response in Markdown, with separate subsections for management team and investors."""

        prompt = f"""Based on the following data, create a team and key stakeholders section for {data["company_name"]}.
        
        Company URL: {data["url"]}
        
        LinkedIn Data: 
        - Employees: {json.dumps(data.get("linkedin_data", {}).get("employees", []), indent=2)}
        
        Website Data: {json.dumps(data.get("website_data", {}).get("team", {}), indent=2)}
        
        Funding Data: {json.dumps(data.get("funding_data", {}).get("investors", []), indent=2)}
        
        Search Data: {json.dumps(data.get("search_data", {}).get("team executives management", {}), indent=2)}
        
        Research Data: {json.dumps(data.get("research_data", {}).get("team", {}), indent=2)}
        """

        return await self._call_llm(prompt, system_prompt)

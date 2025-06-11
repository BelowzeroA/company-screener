import os
from typing import Dict, Any
import json

from app.core.llm_api_wrapper import LLMAPIWrapper
from app.data_sources.openai_websearch import OpenaiWebSearch

SYSTEM_PROMPT = """You are a market analyst creating a market report for a company."""

SECTION_PROMPT = """
You are an expert market analyst. Given the following structured market information:
---
{data}
---
Write a concise market overview report in Markdown
Format the entire output as Markdown, using bullet points if appropriate.  
If data contains numbers, use them.
DO NOT invent information, base all content only on the provided data.
DO NOT include the company name in the report.
DO NOT mention source links.
"""

MARKET_DESCRIPTION_PROMPT = """
Given the following company description, rewrite it as a generic market description suitable for market research queries.
Focus on the type of market and the main activities, not the company name.
The resulting description must be short, one sentence long, 6 - 15 words.
Company market description:
---
{raw_market_description}
---
Market description for search queries:
"""


class MarketProcessor:
    """Class for processing data using LLMs """

    def __init__(self, llm: LLMAPIWrapper):
        """
        Initialize the LLM processor.

        Args:
            llm: LLMAPIWrapper instance for making API calls
        """
        self.llm = llm
        self.searcher = OpenaiWebSearch(llm=llm, logger=None)  # Assuming logger is not needed here

    async def _call_llm(self, prompt: str) -> str:
        """
        Call the OpenAI API with a prompt.

        Args:
            prompt: User prompt to send to the API
            system_prompt: Optional system prompt to provide context

        Returns:
            Generated text response
        """
        response = await self.llm.get_response(
            system_prompt=SYSTEM_PROMPT,
            prompt=prompt,
        )
        return response

    async def search(self, topic: str) -> Dict[str, Any]:
        """
        Search for information on the company's website.

        Args:
            topic: Topic to search for

        Returns:
            Dictionary with the search results
        """
        answer = await self.searcher.search_on_web(topic)
        return answer.dict() if answer else {"content": "N/A"}

    async def generate(self, data: Dict[str, Any]) -> str:
        """
        Generate the market research section.
        Collects data from web using the OpenAI web searcher and formats it into a Markdown report.
        As the market description we use the content from the website data.
        Parameters we want to collect
         - Total Addressable Market (TAM),
         - market segments,
         - CAGR (Compound Annual Growth Rate)
         - geographic expansion.
        When building search queries, we use the company name and the market description.
        The market description can be something like "Company operates in the cryptocurrency exchange market, offering services such as spot trading, futures, margin trading, and staking for various cryptocurrencies."
        Makes separate searches for each of the parameters. and then aggregates them into a single report.
        If exact figures are not available, we provide reasonable estimates based on the industry and similar companies.

        Formats the report in Markdown.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted market research
        """
        company_name = data.get("company_name", "")
        raw_market_description = data.get("website_data", {}).get("market", {}).get("content", "")

        # Use LLM to rewrite the market description for search queries
        rewrite_prompt = MARKET_DESCRIPTION_PROMPT.replace("{raw_market_description}", raw_market_description)
        market_description = await self._call_llm(rewrite_prompt)

        parameters = [
            ("Total Addressable Market (TAM)", f"What is the total addressable market (TAM) for '{market_description}'? Provide recent figures or best estimates."),
            ("Market Segments", f"What are the main market segments for '{market_description}'? List and briefly describe them."),
            ("CAGR", f"What is the Compound Annual Growth Rate (CAGR) for '{market_description}'? Provide recent figures or best estimates."),
            ("Geographic Expansion", f"What are the main geographic regions for '{market_description}'? Are there notable trends in geographic expansion?")
        ]

        # Run searches for all parameters asynchronously
        import asyncio
        async def fetch_param(key, query):
            search_result = await self.search(query)
            return key, search_result.get("content", "N/A")
        tasks = [fetch_param(key, query) for key, query in parameters]
        results_list = await asyncio.gather(*tasks)
        results = {k: v for k, v in results_list}

        # Prepare structured data for LLM
        llm_data = {
            "company_name": company_name,
            "market_description": market_description,
            "parameters": {k: results[k] for k, _ in parameters}
        }
        llm_prompt = SECTION_PROMPT.format(data=json.dumps(llm_data, ensure_ascii=False, indent=2))
        report = await self._call_llm(llm_prompt)
        return report

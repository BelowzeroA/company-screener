import os
from typing import Dict, Any
import json

from app.core.llm_api_wrapper import LLMAPIWrapper


SYSTEM_PROMPT = """You are a product analyst creating a company product section for a report.
Write a concise but informative company overview in 4-6 lines.
Include the product's main features, technology, and any unique aspects that set it apart in the market.
Format your response in Markdown."""

SECTION_PROMPT = """
You are an expert business analyst. Given the following structured company information:
---
{data}
---
Write a comprehensive product overview report in Markdown:
Format the entire output as Markdown, using bullet points if appropriate.  
Do not invent information, base all content only on the provided data.
"""

class ProductProcessor:
    """Class for processing data using LLMs """

    def __init__(self, llm: LLMAPIWrapper):
        """
        Initialize the LLM processor.

        Args:
            llm: LLMAPIWrapper instance for making API calls
        """
        self.llm = llm

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

    async def generate(self, data: Dict[str, Any]) -> str:
        """
        Generate the company overview section.

        Args:
            data: Raw data collected from various sources

        Returns:
            Markdown formatted company overview
        """
        prompt = SECTION_PROMPT.replace(
            "{data}", json.dumps(data)
        )
        return await self._call_llm(prompt)
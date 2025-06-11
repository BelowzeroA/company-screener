import os
from typing import Dict, Any
import json

from app.core.llm_api_wrapper import LLMAPIWrapper


SYSTEM_PROMPT = """You are a financial analyst creating a company overview section for a report.
Write a concise but informative company overview in 4-6 lines.
Include the company's business model, geography, stage, and uniqueness.
Format your response in Markdown."""

SECTION_PROMPT = """
You are an expert business analyst. Given the following structured company information:

{data}

Write a comprehensive company overview report in Markdown, covering these sections **only if the information is present in the data**:

1. # [Company Name]
   - Include company name as the main header.

2. [Website]
   - Add a link to the official website if provided.

3. ## Core Technology & Product
   - Briefly describe what the company does, its main technology, product(s), and unique features.

4. ## Company Profile
   - Include key company facts such as year founded, founders, headquarters, industry focus, and other notable facts.

5. ## Funding & Valuation
   - List latest funding rounds, key investors, valuation, and estimated revenue.

6. ## Market Position & Traction
   - Mention any reported traction, product status (e.g., beta, live), expansion plans, and significant partnerships or customers.

7. ## Strategic Focus
   - Summarize the company’s goals, sustainability initiatives, and its strategic direction.

8. ## Leadership
   - Name key executives, founders, and recent major hires.

9. ## Risks & Challenges
   - Outline risks and challenges mentioned or implied, including competition, technology, or execution risks.

10. ## Industry Context & Growth Potential
    - Add industry background, growth projections, and how the company fits into the broader market.

If any section’s information is not available in the data, **omit that section entirely** from the report.  
Format the entire output as Markdown, using section headers and bullet points as appropriate.  
Do not invent information, base all content only on the provided data.

---
"""

class OverviewProcessor:
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
        # prompt = f"""Based on the following data, create a company overview section for {data["company_name"]}.
        #
        # Company URL: {data["url"]}
        #
        # Website Data: {json.dumps(data.get("website_data", {}).get("home", {}), indent=2)}
        #
        # About Page: {json.dumps(data.get("website_data", {}).get("about", {}), indent=2)}
        #
        # LinkedIn Data: {json.dumps(data.get("linkedin_data", {}).get("company_profile", {}), indent=2)}
        #
        # Search Data: {json.dumps(data.get("search_data", {}).get("company overview", {}), indent=2)}
        # """

        prompt = SECTION_PROMPT.replace(
            "{data}", json.dumps(data)
        )
        return await self._call_llm(prompt)
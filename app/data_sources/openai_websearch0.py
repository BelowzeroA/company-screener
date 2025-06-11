import re
from pydantic import BaseModel, HttpUrl
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.core.openai_api import openai_client, get_openai_response


class WebSearchResponse(BaseModel):
    """Model for web search response."""
    content: str
    link: HttpUrl


SEARCH_WEBSITE_PROMPT = (
    "Search web pages for topic: '{topic}' from a company website '{website_url}'"
    "Also return the webpage link your found the required information on\n"
    "1. Search for pages only within '{website_url}' domain\n"
    "2. Return a clear answer to the topic. If the topic is not present on the website, return N/A \n"
    "3. No pre-text or post-text, just the answer\n"
    "The output must be the following json:\n"
    "```json\n"
    "{{\n"
    "  \"content\": \"<answer>\",\n"
    "  \"link\": \"<link to the page>\"\n"
    "}}\n"
)


class OpenaiWebSearch:

    def __init__(self, llm, logger):
        self.logger = logger
        self.llm = llm
        # Initialize PydanticAI agent with OpenAI model
        self.agent = Agent(
            model=OpenAIModel(
                'gpt-4.1-2025-04-14',
                provider=OpenAIProvider(
                    openai_client=openai_client
                )
            ),
            output_type=WebSearchResponse
        )

    async def search_on_website(self, topic: str, website_url: str) -> WebSearchResponse:
        """
        Search for information on a specific website.

        Args:
            topic: The topic to search for
            website_url: The website URL to search within

        Returns:
            WebSearchResponse containing the search result and source link
        """
        prompt = SEARCH_WEBSITE_PROMPT.replace(
            "{topic}", topic
        ).replace(
            "{website_url}", website_url
        )

        try:
            # Use PydanticAI agent to get validated response
            result = await self.agent.run(prompt)
            return result.output
        except Exception as e:
            self.logger.error(f"Failed to get web search response: {str(e)}")
            raise ValueError(f"Failed to get valid response: {str(e)}")


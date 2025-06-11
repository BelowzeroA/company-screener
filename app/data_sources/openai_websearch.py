import json
import re

from langchain_core.utils.json import parse_json_markdown
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

from app.constants import settings
from app.core.llm_api_wrapper import LLMAPIWrapper

SEARCH_MODEL = "gpt-4o-search-preview"

class WebSearchResponse(BaseModel):
    content: str = Field(
        description="The answer to the topic, found on the specified company website. If not found, use 'N/A'."
    )
    link: str = Field(
        description="Direct URL to the web page where the answer was found. If not found, use 'N/A'."
    )


SEARCH_WEBSITE_PROMPT = (
    """Search web pages for topic: '{topic}' from a company website '{website_url}'
Also return the webpage link your found the required information on
1. Search for pages only within '{website_url}' domain
2. Return a clear answer to the topic. If the topic is not present on the website, return N/A
3. No pre-text or post-text, just the answer
The output must be the following json:
```json
{
  "content": "<answer>",
  "link": "<link to the page>"
}"""
)

SEARCH_WEB_PROMPT = (
    """Search web for topic: '{topic}'
Also return the webpage links your found the required information on
1. Return a clear answer to the topic. If the topic is not present on the website, return N/A
2. No pre-text or post-text, just the answer
The output must be the following json:
```json
{
  "content": "<answer>",
  "link": "<link to the page>"
}"""
)


def strip_utm_source(url):
    return re.split(r'\?utm_[^&\s\)]*', url)[0]


def extract_clean_links(text):
    # Extract Markdown links like [text](https://example.com)
    markdown_links = re.findall(r'\[.*?\]\((https?://[^\s\)]+)\)', text)

    # Extract plain links (not in Markdown format)
    plain_links = re.findall(r'(?<!\()(?<!\])\bhttps?://[^\s\)]+', text)

    all_links = markdown_links + plain_links
    clean_links = []

    for link in all_links:
        # Remove tracking parameters like ?utm_source=
        link = strip_utm_source(link)
        clean_links.append(link)

    return clean_links

class OpenaiWebSearch:

    def __init__(self, llm: LLMAPIWrapper, logger):
        self.logger = logger
        self.llm = llm
        # provider = OpenAIProvider(api_key=settings.openai_api_key)
        # self.model = OpenAIModel("gpt-4o-search-preview", provider=provider)

    async def search_on_website_pydai(self, topic: str, website_url: str) -> WebSearchResponse:
        prompt = SEARCH_WEBSITE_PROMPT.replace(
            "{topic}", topic
        ).replace(
            "{website_url}", website_url
        )
        agent = Agent(model=self.model)
        try:
            response = await agent.run(
                prompt,
                output_type=WebSearchResponse
            )
        except Exception as e:
            self.logger.error(f"Error during web search: {e}")
            return WebSearchResponse(content="N/A", link="N/A")
        return response

    async def search_on_website(self, topic: str, website_url: str) -> WebSearchResponse:
        prompt = SEARCH_WEBSITE_PROMPT.replace(
            "{topic}", topic
        ).replace(
            "{website_url}", website_url
        )

        try:
            response = await self.llm.get_response(
                model=SEARCH_MODEL,
                prompt=prompt,
            )

            data = parse_json_markdown(response)
            result = WebSearchResponse(**data)
        except Exception as e:
            self.logger.error(f"Error during web search: {e}")
            return WebSearchResponse(content="N/A", link="N/A")

        return result

    async def search_on_web(self, topic: str) -> WebSearchResponse:
        prompt = SEARCH_WEB_PROMPT.replace(
            "{topic}", topic
        )

        try:
            response = await self.llm.get_response(
                model=SEARCH_MODEL,
                prompt=prompt,
            )

            if isinstance(response, dict):
                response = response.get("content", "")

            data = parse_json_markdown(response)
            result = WebSearchResponse(**data)
        except Exception as e:
            self.logger.error(f"Error during web search: {e}")
            return WebSearchResponse(content="N/A", link="N/A")

        return result

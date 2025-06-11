"""
LLM aggregator for generating structured content using LLMs.
"""
import os
from typing import Dict, Any
import httpx

class LLMAggregator:
    """Class for generating text content using LLMs."""

    def __init__(self, api_key: str = None, model: str = "gpt-4o"):
        """
        Initialize the LLM aggregator.

        Args:
            api_key: OpenAI API key (defaults to environment variable)
            model: LLM model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required for the LLM aggregator")

        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        self.model = model

    async def generate_content(self, prompt: str, system_prompt: str = None, temperature: float = 0.2) -> str:
        """
        Generate content using the LLM.

        Args:
            prompt: User prompt to send to the API
            system_prompt: Optional system prompt to provide context
            temperature: Creativity level (higher = more creative, lower = more consistent)

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
            "temperature": temperature
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

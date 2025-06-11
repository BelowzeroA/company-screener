import asyncio
import logging
from openai import AsyncOpenAI, RateLimitError

from app.constants import OPENAI_MODEL, settings

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.ERROR)

MODEL_COSTS = {
    "gpt-4.1-2025-04-14": {
        "prompt": 2.0,
        "completion": 8.0,
    },
    "gpt-4o-2024-11-20": {
        "prompt": 2.5,
        "completion": 10.0,
    },
    "gpt-4o-2024-05-13": {
        "prompt": 5.0,
        "completion": 15.0,
    },
    "o1-mini": {
        "prompt": 3.0,
        "completion": 12.0,
    },
    "o1-preview": {
        "prompt": 15.0,
        "completion": 60.0,
    },
    "gpt-4o": {
        "prompt": 2.5,
        "completion": 10.0,
    },
    "gpt-4o-mini": {
        "prompt": 0.15,
        "completion": 0.6,
    },
    "gpt-4o-search-preview": {
        "prompt": 2.5,
        "completion": 10.0,
    }
}


class OpenAIClient:
    _instance = None

    def __new__(cls):
        api_key = settings.openai_api_key
        if cls._instance is None:
            if not api_key or not isinstance(api_key, str):
                raise ValueError("API key is invalid. Please provide a valid OpenAI API key.")
            # if not base_url or not isinstance(base_url, str) or not base_url.startswith("http"):
            #     raise ValueError(
            #         "Proxy URL is invalid. Please provide a valid proxy URL starting with 'http' or 'https'.")

            # cls._instance = AsyncOpenAI(api_key=api_key, base_url=base_url)
            cls._instance = AsyncOpenAI(api_key=api_key)

        return cls._instance


openai_client = OpenAIClient()


async def get_openai_response(
    prompt: str,
    system_prompt: str = None,
    max_tokens: int = 4096,
    model: str = OPENAI_MODEL
):
    """
    Send a request to the OpenAI API and return the response.
    If a 429 error (rate limit) is encountered, retry with exponential backoff.
    """
    system_prompt = system_prompt or "You are an AI publishing assistant"

    max_retries = 5
    backoff_seconds = 1

    for attempt in range(max_retries):
        try:
            if model.startswith("o1-") or model.startswith("gpt-4o-search"):
                # For "o1-" models, send only a user prompt
                response = await openai_client.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": prompt
                                }
                            ]
                        }
                    ]
                )
            else:
                # For other models, include a system prompt and user prompt
                response = await openai_client.chat.completions.create(
                    model=model,
                    max_tokens=max_tokens,
                    temperature=0.5,
                    seed=666,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt},
                    ],
                )

            # If we got here without raising an exception, return the response
            return response

        except Exception as exc:
            # Handle 429 (rate limit) specifically
            if isinstance(exc, RateLimitError):
                if attempt < max_retries - 1:
                    logging.warning(
                        f"Rate limit hit. Retrying in {backoff_seconds} seconds..."
                    )
                    await asyncio.sleep(backoff_seconds)
                    backoff_seconds *= 2  # Exponential backoff
                else:
                    logging.error("Max retries reached. Raising the exception.")
                    raise
            else:
                # If it's not a 429, re-raise the exception
                raise

    # If, for some reason, we break out of the loop without returning or raising:
    raise RuntimeError("Unable to get a valid OpenAI response after max retries.")

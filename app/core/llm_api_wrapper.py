import time
from app.core.openai_api import get_openai_response, MODEL_COSTS
from app.constants import OPENAI_MODEL


class LLMAPIWrapper:
    """
    A wrapper for the LLM API.
    """

    def __init__(self):
        self.accumulated_cost = 0

    async def get_response(
        self,
        prompt: str,
        system_prompt: str = None,
        max_tokens: int = 4096,
        model=None
    ):
        time.sleep(1)
        model = model or OPENAI_MODEL
        response = await get_openai_response(prompt, system_prompt, max_tokens, model)

        model_prices = MODEL_COSTS[model]
        prompt_cost = model_prices['prompt'] * response.usage.prompt_tokens
        completion_cost = model_prices['completion'] * response.usage.completion_tokens
        total_cost = (prompt_cost + completion_cost) / 1000000
        self.accumulated_cost += total_cost
        response_message = response.choices[0].message
        if response_message.annotations:
            response = {"annotations": response_message.annotations, "content": response_message.content}
        else:
            response = response_message.content
        return response
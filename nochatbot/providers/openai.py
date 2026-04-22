"""OpenAI provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from nochatbot.providers.base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI provider using the official OpenAI SDK.

    This provider supports GPT-4 and other OpenAI models.
    """

    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview", **kwargs: Any) -> None:
        """Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: OpenAI model identifier (default: gpt-4-turbo-preview)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to OpenAI and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, frequency_penalty)

        Returns:
            The complete response text from OpenAI

        Raises:
            Exception: If the API call fails
        """
        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": message})

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            return response.choices[0].message.content or ""

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from OpenAI token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, frequency_penalty)

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        try:
            messages = []

            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})

            messages.append({"role": "user", "content": message})

            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=True,
                **kwargs
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current OpenAI model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on OpenAI's pricing as of 2025.
            For exact pricing, refer to https://openai.com/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "gpt-4-turbo-preview": {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000},
            "gpt-4": {"input": 30.00 / 1_000_000, "output": 60.00 / 1_000_000},
            "gpt-4-32k": {"input": 60.00 / 1_000_000, "output": 120.00 / 1_000_000},
            "gpt-3.5-turbo": {"input": 0.50 / 1_000_000, "output": 1.50 / 1_000_000},
            "gpt-3.5-turbo-16k": {"input": 3.00 / 1_000_000, "output": 4.00 / 1_000_000},
        }

        # Return pricing for the current model, or default to GPT-4 Turbo pricing
        return pricing_map.get(
            self.model,
            {"input": 10.00 / 1_000_000, "output": 30.00 / 1_000_000}
        )

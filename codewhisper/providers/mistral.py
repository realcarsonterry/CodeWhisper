"""Mistral AI provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from codewhisper.providers.base import AIProvider


class MistralProvider(AIProvider):
    """Mistral AI provider using OpenAI-compatible interface.

    This provider connects to Mistral AI's API using the OpenAI SDK
    with a custom base URL.

    Supported models:
    - mistral-large: Most capable model for complex tasks
    - mistral-medium: Balanced performance and cost
    - mistral-small: Fast and cost-effective
    """

    def __init__(self, api_key: str, model: str = "mistral-large-latest", **kwargs: Any) -> None:
        """Initialize the Mistral provider.

        Args:
            api_key: Mistral AI API key
            model: Mistral model identifier (default: mistral-large-latest)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.mistral.ai/v1"
        )

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Mistral and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

        Returns:
            The complete response text from Mistral

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
            raise Exception(f"Mistral API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Mistral token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

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
            raise Exception(f"Mistral API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Mistral model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Mistral AI's pricing as of 2025.
            For exact pricing, refer to https://mistral.ai/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "mistral-large-latest": {"input": 4.00 / 1_000_000, "output": 12.00 / 1_000_000},
            "mistral-medium-latest": {"input": 2.70 / 1_000_000, "output": 8.10 / 1_000_000},
            "mistral-small-latest": {"input": 1.00 / 1_000_000, "output": 3.00 / 1_000_000},
        }

        # Return pricing for the current model, or default to mistral-large pricing
        return pricing_map.get(
            self.model,
            {"input": 4.00 / 1_000_000, "output": 12.00 / 1_000_000}
        )

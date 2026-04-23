"""Moonshot (Kimi) provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from codewhisper.providers.base import AIProvider


class MoonshotProvider(AIProvider):
    """Moonshot (Kimi) provider using OpenAI-compatible interface.

    This provider connects to Moonshot AI's API using the OpenAI SDK
    with a custom base URL. Moonshot is known for its long-context models.

    Supported models:
    - moonshot-v1-8k: 8K context window
    - moonshot-v1-32k: 32K context window
    - moonshot-v1-128k: 128K context window for long documents
    """

    def __init__(self, api_key: str, model: str = "moonshot-v1-32k", **kwargs: Any) -> None:
        """Initialize the Moonshot provider.

        Args:
            api_key: Moonshot AI API key
            model: Moonshot model identifier (default: moonshot-v1-32k)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.moonshot.cn/v1"
        )

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Moonshot and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

        Returns:
            The complete response text from Moonshot

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
            raise Exception(f"Moonshot API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Moonshot token by token.

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
            raise Exception(f"Moonshot API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Moonshot model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Moonshot AI's pricing as of 2025.
            Prices are converted from CNY to USD (1 CNY ≈ 0.14 USD).
            For exact pricing, refer to https://platform.moonshot.cn/docs/pricing
        """
        # Pricing per million tokens (approximate conversion from CNY)
        pricing_map = {
            "moonshot-v1-8k": {"input": 1.68 / 1_000_000, "output": 1.68 / 1_000_000},  # ¥12/M
            "moonshot-v1-32k": {"input": 3.36 / 1_000_000, "output": 3.36 / 1_000_000},  # ¥24/M
            "moonshot-v1-128k": {"input": 8.40 / 1_000_000, "output": 8.40 / 1_000_000},  # ¥60/M
        }

        # Return pricing for the current model, or default to moonshot-v1-32k pricing
        return pricing_map.get(
            self.model,
            {"input": 3.36 / 1_000_000, "output": 3.36 / 1_000_000}
        )

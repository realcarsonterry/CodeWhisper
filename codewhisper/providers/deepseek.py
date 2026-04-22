"""DeepSeek AI provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from codewhisper.providers.base import AIProvider


class DeepSeekProvider(AIProvider):
    """DeepSeek AI provider using OpenAI-compatible interface.

    This provider connects to DeepSeek's API using the OpenAI SDK
    with a custom base URL.
    """

    def __init__(self, api_key: str, model: str = "deepseek-chat", **kwargs: Any) -> None:
        """Initialize the DeepSeek provider.

        Args:
            api_key: DeepSeek API key
            model: DeepSeek model identifier (default: deepseek-chat)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to DeepSeek and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, frequency_penalty)

        Returns:
            The complete response text from DeepSeek

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
            raise Exception(f"DeepSeek API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from DeepSeek token by token.

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
            raise Exception(f"DeepSeek API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current DeepSeek model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on DeepSeek's pricing.
            For exact pricing, refer to https://platform.deepseek.com/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "deepseek-chat": {"input": 0.14 / 1_000_000, "output": 0.28 / 1_000_000},
            "deepseek-coder": {"input": 0.14 / 1_000_000, "output": 0.28 / 1_000_000},
        }

        # Return pricing for the current model, or default to deepseek-chat pricing
        return pricing_map.get(
            self.model,
            {"input": 0.14 / 1_000_000, "output": 0.28 / 1_000_000}
        )

"""Qwen (通义千问) provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from codewhisper.providers.base import AIProvider


class QwenProvider(AIProvider):
    """Qwen (通义千问) provider using OpenAI-compatible interface.

    This provider connects to Alibaba Cloud's Qwen API using the OpenAI SDK
    with a custom base URL. Qwen is developed by Alibaba Cloud.

    Supported models:
    - qwen-max: Most capable model for complex reasoning
    - qwen-plus: Balanced performance and cost
    - qwen-turbo: Fast and cost-effective
    """

    def __init__(self, api_key: str, model: str = "qwen-max", **kwargs: Any) -> None:
        """Initialize the Qwen provider.

        Args:
            api_key: Alibaba Cloud DashScope API key
            model: Qwen model identifier (default: qwen-max)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
        )

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Qwen and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

        Returns:
            The complete response text from Qwen

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
            raise Exception(f"Qwen API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Qwen token by token.

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
            raise Exception(f"Qwen API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Qwen model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Alibaba Cloud's pricing as of 2025.
            Prices are converted from CNY to USD (1 CNY ≈ 0.14 USD).
            For exact pricing, refer to https://help.aliyun.com/zh/dashscope/
        """
        # Pricing per million tokens (approximate conversion from CNY)
        pricing_map = {
            "qwen-max": {"input": 0.56 / 1_000_000, "output": 1.68 / 1_000_000},  # ¥4/M input, ¥12/M output
            "qwen-plus": {"input": 0.28 / 1_000_000, "output": 0.84 / 1_000_000},  # ¥2/M input, ¥6/M output
            "qwen-turbo": {"input": 0.042 / 1_000_000, "output": 0.126 / 1_000_000},  # ¥0.3/M input, ¥0.9/M output
        }

        # Return pricing for the current model, or default to qwen-max pricing
        return pricing_map.get(
            self.model,
            {"input": 0.56 / 1_000_000, "output": 1.68 / 1_000_000}
        )

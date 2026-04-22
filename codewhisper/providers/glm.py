"""GLM (Zhipu AI) provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from openai import AsyncOpenAI
from .base import AIProvider


class GLMProvider(AIProvider):
    """GLM (Zhipu AI) provider using OpenAI-compatible interface.

    Zhipu AI provides GLM models through an OpenAI-compatible API.
    This provider uses the OpenAI SDK with a custom base URL.

    Supported models:
    - glm-4-plus: Most capable model
    - glm-4-0520: Balanced performance
    - glm-4-air: Fast and cost-effective
    - glm-4-airx: Ultra-fast
    - glm-4-flash: Fastest
    """

    def __init__(self, api_key: str, model: str = "glm-4-plus", **kwargs: Any) -> None:
        """Initialize GLM provider.

        Args:
            api_key: Zhipu AI API key
            model: Model to use (default: glm-4-plus)
            **kwargs: Additional configuration
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters

        Returns:
            The complete response text

        Raises:
            Exception: If the API call fails
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"GLM API error: {str(e)}")

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": message})

        try:
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
            raise Exception(f"GLM API streaming error: {str(e)}")

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for GLM models.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Pricing as of 2024 (approximate, converted from CNY):
            - glm-4-plus: ¥0.05/1K tokens input, ¥0.05/1K tokens output
            - glm-4-0520: ¥0.10/1K tokens input, ¥0.10/1K tokens output
            - glm-4-air: ¥0.001/1K tokens input, ¥0.001/1K tokens output
            - glm-4-airx: ¥0.001/1K tokens input, ¥0.001/1K tokens output
            - glm-4-flash: ¥0.0001/1K tokens input, ¥0.0001/1K tokens output
        """
        # Pricing in USD (approximate conversion: 1 CNY ≈ 0.14 USD)
        pricing = {
            "glm-4-plus": {"input": 0.000007, "output": 0.000007},      # ~¥0.05/1K
            "glm-4-0520": {"input": 0.000014, "output": 0.000014},      # ~¥0.10/1K
            "glm-4-air": {"input": 0.00000014, "output": 0.00000014},   # ~¥0.001/1K
            "glm-4-airx": {"input": 0.00000014, "output": 0.00000014},  # ~¥0.001/1K
            "glm-4-flash": {"input": 0.000000014, "output": 0.000000014}, # ~¥0.0001/1K
        }

        return pricing.get(self.model, {"input": 0.000007, "output": 0.000007})

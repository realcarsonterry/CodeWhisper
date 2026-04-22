"""Claude AI provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
import anthropic
from codewhisper.providers.base import AIProvider


class ClaudeProvider(AIProvider):
    """Claude AI provider using the Anthropic SDK.

    This provider supports Claude models including claude-opus-4-20250514.
    It implements both streaming and non-streaming message generation.
    """

    def __init__(self, api_key: str, model: str = "claude-opus-4-20250514", **kwargs: Any) -> None:
        """Initialize the Claude provider.

        Args:
            api_key: Anthropic API key
            model: Claude model identifier (default: claude-opus-4-20250514)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = anthropic.AsyncAnthropic(api_key=api_key)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Claude and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, top_k)

        Returns:
            The complete response text from Claude

        Raises:
            anthropic.APIError: If the API call fails
        """
        try:
            request_params: Dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": message}],
            }

            if system_prompt:
                request_params["system"] = system_prompt

            # Add any additional parameters
            request_params.update(kwargs)

            response = await self.client.messages.create(**request_params)

            # Extract text from content blocks
            return "".join(
                block.text for block in response.content if hasattr(block, "text")
            )

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Claude token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, top_k)

        Yields:
            Response text chunks as they arrive

        Raises:
            anthropic.APIError: If the API call fails
        """
        try:
            request_params: Dict[str, Any] = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": [{"role": "user", "content": message}],
            }

            if system_prompt:
                request_params["system"] = system_prompt

            # Add any additional parameters
            request_params.update(kwargs)

            async with self.client.messages.stream(**request_params) as stream:
                async for text in stream.text_stream:
                    yield text

        except anthropic.APIError as e:
            raise Exception(f"Claude API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Claude model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Anthropic's pricing as of 2025.
            For exact pricing, refer to https://www.anthropic.com/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "claude-opus-4-20250514": {"input": 15.00 / 1_000_000, "output": 75.00 / 1_000_000},
            "claude-sonnet-4-20250514": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
            "claude-3-5-sonnet-20241022": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
            "claude-3-opus-20240229": {"input": 15.00 / 1_000_000, "output": 75.00 / 1_000_000},
        }

        # Return pricing for the current model, or default to Opus pricing
        return pricing_map.get(
            self.model,
            {"input": 15.00 / 1_000_000, "output": 75.00 / 1_000_000}
        )

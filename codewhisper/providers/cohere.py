"""Cohere provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
import cohere
from codewhisper.providers.base import AIProvider


class CohereProvider(AIProvider):
    """Cohere provider using the official Cohere SDK.

    This provider supports Cohere's Command models including command,
    command-r, and command-r-plus for chat and text generation.

    Supported models:
    - command: Base command model
    - command-r: Retrieval-augmented generation model
    - command-r-plus: Enhanced RAG model with better performance
    """

    def __init__(self, api_key: str, model: str = "command-r-plus", **kwargs: Any) -> None:
        """Initialize the Cohere provider.

        Args:
            api_key: Cohere API key
            model: Cohere model identifier (default: command-r-plus)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = cohere.AsyncClient(api_key=api_key)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Cohere and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., p, k, frequency_penalty)

        Returns:
            The complete response text from Cohere

        Raises:
            Exception: If the API call fails
        """
        try:
            request_params: Dict[str, Any] = {
                "model": self.model,
                "message": message,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            if system_prompt:
                request_params["preamble"] = system_prompt

            # Add any additional parameters
            request_params.update(kwargs)

            response = await self.client.chat(**request_params)

            return response.text

        except Exception as e:
            raise Exception(f"Cohere API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Cohere token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., p, k, frequency_penalty)

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        try:
            request_params: Dict[str, Any] = {
                "model": self.model,
                "message": message,
                "temperature": temperature,
                "max_tokens": max_tokens,
            }

            if system_prompt:
                request_params["preamble"] = system_prompt

            # Add any additional parameters
            request_params.update(kwargs)

            stream = await self.client.chat_stream(**request_params)

            async for event in stream:
                if event.event_type == "text-generation":
                    yield event.text

        except Exception as e:
            raise Exception(f"Cohere API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Cohere model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Cohere's pricing as of 2025.
            For exact pricing, refer to https://cohere.com/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "command": {"input": 1.00 / 1_000_000, "output": 2.00 / 1_000_000},
            "command-r": {"input": 0.50 / 1_000_000, "output": 1.50 / 1_000_000},
            "command-r-plus": {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000},
        }

        # Return pricing for the current model, or default to command-r-plus pricing
        return pricing_map.get(
            self.model,
            {"input": 3.00 / 1_000_000, "output": 15.00 / 1_000_000}
        )

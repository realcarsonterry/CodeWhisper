"""Google Gemini provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
import warnings
import os

# Suppress the deprecation warning before importing
os.environ['PYTHONWARNINGS'] = 'ignore::FutureWarning'
warnings.filterwarnings('ignore', category=FutureWarning)

import google.generativeai as genai
from codewhisper.providers.base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini provider using the google-generativeai SDK.

    This provider supports Gemini models including gemini-pro, gemini-1.5-pro,
    and gemini-1.5-flash. It implements both streaming and non-streaming generation.

    Supported models:
    - gemini-pro: Original Gemini Pro model
    - gemini-1.5-pro: Latest pro model with extended context
    - gemini-1.5-flash: Fast and efficient model
    """

    def __init__(self, api_key: str, model: str = "gemini-1.5-pro", **kwargs: Any) -> None:
        """Initialize the Gemini provider.

        Args:
            api_key: Google AI API key
            model: Gemini model identifier (default: gemini-1.5-pro)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel(model)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Gemini and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, top_k)

        Returns:
            The complete response text from Gemini

        Raises:
            Exception: If the API call fails
        """
        try:
            # Combine system prompt with user message if provided
            full_message = message
            if system_prompt:
                full_message = f"{system_prompt}\n\n{message}"

            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )

            response = await self.client.generate_content_async(
                full_message,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Gemini token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, top_k)

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        try:
            # Combine system prompt with user message if provided
            full_message = message
            if system_prompt:
                full_message = f"{system_prompt}\n\n{message}"

            generation_config = genai.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens,
                **kwargs
            )

            response = await self.client.generate_content_async(
                full_message,
                generation_config=generation_config,
                stream=True
            )

            async for chunk in response:
                if chunk.text:
                    yield chunk.text

        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Gemini model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Google's pricing as of 2025.
            For exact pricing, refer to https://ai.google.dev/pricing
        """
        # Pricing per million tokens (as of 2025)
        pricing_map = {
            "gemini-pro": {"input": 0.50 / 1_000_000, "output": 1.50 / 1_000_000},
            "gemini-1.5-pro": {"input": 1.25 / 1_000_000, "output": 5.00 / 1_000_000},
            "gemini-1.5-flash": {"input": 0.075 / 1_000_000, "output": 0.30 / 1_000_000},
        }

        # Return pricing for the current model, or default to gemini-1.5-pro pricing
        return pricing_map.get(
            self.model,
            {"input": 1.25 / 1_000_000, "output": 5.00 / 1_000_000}
        )

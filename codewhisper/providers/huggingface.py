"""Hugging Face provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
from huggingface_hub import AsyncInferenceClient
from codewhisper.providers.base import AIProvider


class HuggingFaceProvider(AIProvider):
    """Hugging Face provider using the huggingface_hub SDK.

    This provider supports any text generation model available on Hugging Face Hub.
    It uses the Inference API for serverless inference.

    Popular models:
    - meta-llama/Meta-Llama-3-70B-Instruct
    - mistralai/Mixtral-8x7B-Instruct-v0.1
    - google/gemma-7b-it
    - microsoft/phi-2
    """

    def __init__(self, api_key: str, model: str = "meta-llama/Meta-Llama-3-70B-Instruct", **kwargs: Any) -> None:
        """Initialize the Hugging Face provider.

        Args:
            api_key: Hugging Face API token
            model: Model identifier on Hugging Face Hub (default: meta-llama/Meta-Llama-3-70B-Instruct)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)
        self.client = AsyncInferenceClient(token=api_key)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to Hugging Face model and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p, top_k)

        Returns:
            The complete response text from the model

        Raises:
            Exception: If the API call fails
        """
        try:
            # Combine system prompt with user message if provided
            full_message = message
            if system_prompt:
                full_message = f"<|system|>\n{system_prompt}\n<|user|>\n{message}\n<|assistant|>"

            response = await self.client.text_generation(
                prompt=full_message,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                return_full_text=False,
                **kwargs
            )

            return response

        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from Hugging Face model token by token.

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
                full_message = f"<|system|>\n{system_prompt}\n<|user|>\n{message}\n<|assistant|>"

            stream = await self.client.text_generation(
                prompt=full_message,
                model=self.model,
                max_new_tokens=max_tokens,
                temperature=temperature,
                stream=True,
                return_full_text=False,
                **kwargs
            )

            async for chunk in stream:
                if hasattr(chunk, 'token') and hasattr(chunk.token, 'text'):
                    yield chunk.token.text
                elif isinstance(chunk, str):
                    yield chunk

        except Exception as e:
            raise Exception(f"Hugging Face API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current Hugging Face model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Hugging Face Inference API pricing varies by model and usage tier.
            Free tier has rate limits. Pro tier costs $9/month with higher limits.
            Dedicated endpoints have custom pricing.

            These are approximate costs for reference. For exact pricing,
            refer to https://huggingface.co/pricing
        """
        # Approximate pricing for popular models (per million tokens)
        # Note: Many models on HF are free with rate limits
        pricing_map = {
            "meta-llama/Meta-Llama-3-70B-Instruct": {"input": 0.65 / 1_000_000, "output": 2.75 / 1_000_000},
            "mistralai/Mixtral-8x7B-Instruct-v0.1": {"input": 0.50 / 1_000_000, "output": 1.50 / 1_000_000},
            "google/gemma-7b-it": {"input": 0.10 / 1_000_000, "output": 0.30 / 1_000_000},
            "microsoft/phi-2": {"input": 0.05 / 1_000_000, "output": 0.15 / 1_000_000},
        }

        # Return pricing for the current model, or default to free tier (0 cost)
        return pricing_map.get(
            self.model,
            {"input": 0.0, "output": 0.0}
        )

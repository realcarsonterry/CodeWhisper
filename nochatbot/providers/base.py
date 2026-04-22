"""Base provider interface for AI providers."""

from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncIterator, Optional


class AIProvider(ABC):
    """Abstract base class for AI providers.

    This class defines the unified interface that all AI providers must implement.
    It supports both streaming and non-streaming responses, and provides cost tracking.
    """

    def __init__(self, api_key: str, model: str, **kwargs: Any) -> None:
        """Initialize the AI provider.

        Args:
            api_key: API key for authentication
            model: Model identifier to use
            **kwargs: Additional provider-specific configuration
        """
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
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
            **kwargs: Additional provider-specific parameters

        Returns:
            The complete response text from the AI

        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
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
            **kwargs: Additional provider-specific parameters

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        pass

    @abstractmethod
    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD
        """
        pass

    def calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Calculate the total cost for a request.

        Args:
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens

        Returns:
            Total cost in USD
        """
        costs = self.get_cost_per_token()
        return (input_tokens * costs['input']) + (output_tokens * costs['output'])

"""Mock provider for testing without real API calls."""

from typing import Dict, Any, AsyncIterator, Optional
import asyncio
from .base import AIProvider


class MockProvider(AIProvider):
    """Mock AI provider that returns fake responses for testing.

    This provider doesn't make real API calls and is useful for:
    - Testing the CodeWhisper system without API costs
    - Development and debugging
    - Demonstrating the workflow
    """

    def __init__(self, api_key: str = "mock", model: str = "mock-model", **kwargs: Any) -> None:
        """Initialize mock provider.

        Args:
            api_key: Ignored (can be anything)
            model: Ignored (can be anything)
            **kwargs: Additional configuration (ignored)
        """
        super().__init__(api_key, model, **kwargs)

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Return a mock response.

        Args:
            message: The user message
            system_prompt: Optional system prompt
            temperature: Ignored
            max_tokens: Ignored
            **kwargs: Additional parameters (ignored)

        Returns:
            A mock response based on the message content
        """
        # Simulate API delay
        await asyncio.sleep(0.5)

        # Generate mock response based on message content
        if "summarize" in message.lower() or "what does this file do" in message.lower():
            return "This file contains code that implements core functionality. It includes function definitions, imports, and logic for processing data."
        elif "question" in message.lower():
            return """What aspect of the codebase would you like to explore?

1. Understand the overall architecture
2. Explore the main entry points
3. Review the data models
4. Examine the API endpoints
5. Check the configuration system
6. Analyze the testing strategy
7. Review the documentation
8. Explore the dependencies"""
        else:
            return f"Mock response to: {message[:50]}..."

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a mock response word by word.

        Args:
            message: The user message
            system_prompt: Optional system prompt
            temperature: Ignored
            max_tokens: Ignored
            **kwargs: Additional parameters (ignored)

        Yields:
            Mock response chunks
        """
        response = await self.send_message(message, system_prompt, temperature, max_tokens, **kwargs)

        # Stream word by word
        words = response.split()
        for word in words:
            await asyncio.sleep(0.05)  # Simulate streaming delay
            yield word + " "

    def get_cost_per_token(self) -> Dict[str, float]:
        """Return mock costs (zero).

        Returns:
            Dictionary with input and output costs (both 0)
        """
        return {
            "input": 0.0,
            "output": 0.0
        }

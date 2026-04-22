"""AI Provider layer for No Chat Bot.

This module provides a unified interface for interacting with different AI providers
including Claude (Anthropic), OpenAI, and DeepSeek.

Example usage:
    from nochatbot.providers import ClaudeProvider, OpenAIProvider, DeepSeekProvider

    # Initialize a provider
    provider = ClaudeProvider(api_key="your-api-key", model="claude-opus-4-20250514")

    # Send a message
    response = await provider.send_message("Analyze this code...")

    # Stream a response
    async for chunk in provider.stream_response("Explain this function..."):
        print(chunk, end="", flush=True)

    # Calculate costs
    cost = provider.calculate_cost(input_tokens=1000, output_tokens=500)
"""

from nochatbot.providers.base import AIProvider
from nochatbot.providers.claude import ClaudeProvider
from nochatbot.providers.openai import OpenAIProvider
from nochatbot.providers.deepseek import DeepSeekProvider

__all__ = [
    'AIProvider',
    'ClaudeProvider',
    'OpenAIProvider',
    'DeepSeekProvider',
]

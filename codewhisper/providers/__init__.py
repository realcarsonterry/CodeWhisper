"""AI Provider layer for CodeWhisper.

This module provides a unified interface for interacting with different AI providers
including Claude (Anthropic), OpenAI, DeepSeek, and GLM (Zhipu AI).

Example usage:
    from codewhisper.providers import ClaudeProvider, OpenAIProvider, DeepSeekProvider, GLMProvider

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

from codewhisper.providers.base import AIProvider
from codewhisper.providers.claude import ClaudeProvider
from codewhisper.providers.openai import OpenAIProvider
from codewhisper.providers.deepseek import DeepSeekProvider
from codewhisper.providers.glm import GLMProvider

__all__ = [
    'AIProvider',
    'ClaudeProvider',
    'OpenAIProvider',
    'DeepSeekProvider',
    'GLMProvider',
]

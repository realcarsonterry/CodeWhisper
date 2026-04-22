"""AI Provider layer for CodeWhisper.

This module provides a unified interface for interacting with different AI providers
including Claude (Anthropic), OpenAI, DeepSeek, GLM (Zhipu AI), Google Gemini,
Cohere, Mistral AI, Qwen (通义千问), Moonshot (月之暗面), Baidu ERNIE, and Hugging Face.

Example usage:
    from codewhisper.providers import ClaudeProvider, OpenAIProvider, GeminiProvider

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
from codewhisper.providers.gemini import GeminiProvider
from codewhisper.providers.cohere import CohereProvider
from codewhisper.providers.mistral import MistralProvider
from codewhisper.providers.qwen import QwenProvider
from codewhisper.providers.moonshot import MoonshotProvider
from codewhisper.providers.ernie import ERNIEProvider
from codewhisper.providers.huggingface import HuggingFaceProvider

__all__ = [
    'AIProvider',
    'ClaudeProvider',
    'OpenAIProvider',
    'DeepSeekProvider',
    'GLMProvider',
    'GeminiProvider',
    'CohereProvider',
    'MistralProvider',
    'QwenProvider',
    'MoonshotProvider',
    'ERNIEProvider',
    'HuggingFaceProvider',
]

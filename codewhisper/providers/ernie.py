"""Baidu ERNIE provider implementation."""

from typing import Dict, Any, AsyncIterator, Optional
import aiohttp
import json
from codewhisper.providers.base import AIProvider


class ERNIEProvider(AIProvider):
    """Baidu ERNIE provider using custom API implementation.

    This provider connects to Baidu's ERNIE API using the requests library.
    ERNIE (Enhanced Representation through kNowledge IntEgration) is Baidu's
    large language model series.

    Supported models:
    - ernie-4.0: Most capable model
    - ernie-3.5: Balanced performance
    - ernie-turbo: Fast and cost-effective
    """

    def __init__(self, api_key: str, model: str = "ernie-4.0", **kwargs: Any) -> None:
        """Initialize the ERNIE provider.

        Args:
            api_key: Baidu API key (format: "API_KEY:SECRET_KEY")
            model: ERNIE model identifier (default: ernie-4.0)
            **kwargs: Additional configuration options
        """
        super().__init__(api_key, model, **kwargs)

        # Parse API key and secret
        if ":" in api_key:
            self.api_key_part, self.secret_key = api_key.split(":", 1)
        else:
            self.api_key_part = api_key
            self.secret_key = kwargs.get("secret_key", "")

        self.access_token: Optional[str] = None
        self._model_endpoints = {
            "ernie-4.0": "completions_pro",
            "ernie-3.5": "completions",
            "ernie-turbo": "eb-instant",
        }

    async def _get_access_token(self) -> str:
        """Get access token from Baidu OAuth API.

        Returns:
            Access token string

        Raises:
            Exception: If token retrieval fails
        """
        if self.access_token:
            return self.access_token

        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key_part,
            "client_secret": self.secret_key,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, params=params) as response:
                    if response.status != 200:
                        raise Exception(f"Failed to get access token: {response.status}")

                    data = await response.json()
                    self.access_token = data.get("access_token")

                    if not self.access_token:
                        raise Exception("No access token in response")

                    return self.access_token

        except Exception as e:
            raise Exception(f"ERNIE authentication error: {str(e)}") from e

    def _get_endpoint_url(self) -> str:
        """Get the API endpoint URL for the current model.

        Returns:
            Full API endpoint URL
        """
        endpoint = self._model_endpoints.get(self.model, "completions_pro")
        return f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/{endpoint}"

    async def send_message(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> str:
        """Send a message to ERNIE and get a complete response.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

        Returns:
            The complete response text from ERNIE

        Raises:
            Exception: If the API call fails
        """
        try:
            access_token = await self._get_access_token()
            url = self._get_endpoint_url()

            messages = []
            if system_prompt:
                messages.append({"role": "user", "content": system_prompt})
                messages.append({"role": "assistant", "content": "好的，我明白了。"})

            messages.append({"role": "user", "content": message})

            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                **kwargs
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    params={"access_token": access_token},
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API request failed: {response.status} - {error_text}")

                    data = await response.json()

                    if "error_code" in data:
                        raise Exception(f"ERNIE API error: {data.get('error_msg', 'Unknown error')}")

                    return data.get("result", "")

        except Exception as e:
            raise Exception(f"ERNIE API error: {str(e)}") from e

    async def stream_response(
        self,
        message: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        **kwargs: Any
    ) -> AsyncIterator[str]:
        """Stream a response from ERNIE token by token.

        Args:
            message: The user message to send
            system_prompt: Optional system prompt to set context
            temperature: Sampling temperature (0.0 to 1.0)
            max_tokens: Maximum tokens in the response
            **kwargs: Additional parameters (e.g., top_p)

        Yields:
            Response text chunks as they arrive

        Raises:
            Exception: If the API call fails
        """
        try:
            access_token = await self._get_access_token()
            url = self._get_endpoint_url()

            messages = []
            if system_prompt:
                messages.append({"role": "user", "content": system_prompt})
                messages.append({"role": "assistant", "content": "好的，我明白了。"})

            messages.append({"role": "user", "content": message})

            payload = {
                "messages": messages,
                "temperature": temperature,
                "max_output_tokens": max_tokens,
                "stream": True,
                **kwargs
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    url,
                    params={"access_token": access_token},
                    json=payload,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        raise Exception(f"API request failed: {response.status} - {error_text}")

                    async for line in response.content:
                        line = line.decode('utf-8').strip()
                        if line.startswith("data: "):
                            line = line[6:]  # Remove "data: " prefix

                        if not line:
                            continue

                        try:
                            data = json.loads(line)
                            if "error_code" in data:
                                raise Exception(f"ERNIE API error: {data.get('error_msg', 'Unknown error')}")

                            if "result" in data:
                                yield data["result"]
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            raise Exception(f"ERNIE API error: {str(e)}") from e

    def get_cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for the current ERNIE model.

        Returns:
            Dictionary with 'input' and 'output' keys containing cost per token in USD

        Note:
            Costs are approximate and based on Baidu's pricing as of 2025.
            Prices are converted from CNY to USD (1 CNY ≈ 0.14 USD).
            For exact pricing, refer to https://cloud.baidu.com/doc/WENXINWORKSHOP/s/hlrk4akp7
        """
        # Pricing per million tokens (approximate conversion from CNY)
        pricing_map = {
            "ernie-4.0": {"input": 1.68 / 1_000_000, "output": 1.68 / 1_000_000},  # ¥12/M
            "ernie-3.5": {"input": 0.168 / 1_000_000, "output": 0.168 / 1_000_000},  # ¥1.2/M
            "ernie-turbo": {"input": 0.112 / 1_000_000, "output": 0.112 / 1_000_000},  # ¥0.8/M
        }

        # Return pricing for the current model, or default to ernie-4.0 pricing
        return pricing_map.get(
            self.model,
            {"input": 1.68 / 1_000_000, "output": 1.68 / 1_000_000}
        )

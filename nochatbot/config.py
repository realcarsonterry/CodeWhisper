"""Configuration management for No Chat Bot."""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List


class Config:
    """Configuration manager for No Chat Bot.

    Manages configuration file at ~/.nochatbot/config.json with support for
    multiple AI providers, scanning settings, knowledge base configuration,
    and privacy settings.
    """

    CONFIG_DIR = Path.home() / ".nochatbot"
    CONFIG_FILE = CONFIG_DIR / "config.json"

    def __init__(self):
        """Initialize the configuration manager."""
        self.config: Dict[str, Any] = {}
        self.ensure_config_exists()
        self.load_config()

    def ensure_config_exists(self) -> None:
        """Ensure configuration directory and file exist.

        Creates the configuration directory and file with default settings
        if they don't already exist.

        Raises:
            OSError: If directory or file creation fails.
        """
        try:
            # Create config directory if it doesn't exist
            self.CONFIG_DIR.mkdir(parents=True, exist_ok=True)

            # Create config file with defaults if it doesn't exist
            if not self.CONFIG_FILE.exists():
                default_config = self.get_default_config()
                with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)
        except OSError as e:
            raise OSError(f"Failed to create configuration directory or file: {e}")

    def get_default_config(self) -> Dict[str, Any]:
        """Get the default configuration structure.

        Returns:
            Dictionary containing default configuration settings.
        """
        return {
            "version": "1.0.0",
            "providers": {},
            "scanning": {
                "max_agents": 100,
                "exclude_dirs": [
                    "node_modules",
                    ".git",
                    "__pycache__",
                    ".venv",
                    "venv",
                    "dist",
                    "build"
                ],
                "exclude_files": [
                    "*.pyc",
                    "*.log",
                    ".DS_Store"
                ],
                "max_file_size_mb": 10
            },
            "knowledge_base": {
                "path": "~/.nochatbot/knowledge",
                "vector_db": "chromadb"
            },
            "privacy": {
                "permissions_granted": False,
                "exclude_paths": []
            }
        }

    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file.

        Returns:
            Dictionary containing the loaded configuration.

        Raises:
            json.JSONDecodeError: If configuration file contains invalid JSON.
            OSError: If configuration file cannot be read.
        """
        try:
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            return self.config
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in configuration file: {e.msg}",
                e.doc,
                e.pos
            )
        except OSError as e:
            raise OSError(f"Failed to read configuration file: {e}")

    def save_config(self) -> None:
        """Save current configuration to file.

        Raises:
            OSError: If configuration file cannot be written.
            TypeError: If configuration contains non-serializable objects.
        """
        try:
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except (OSError, TypeError) as e:
            raise type(e)(f"Failed to save configuration: {e}")

    def add_provider(self, name: str, api_key: str, model: Optional[str] = None) -> None:
        """Add or update an AI provider configuration.

        Args:
            name: Provider name (e.g., 'anthropic', 'openai').
            api_key: API key for the provider.
            model: Optional default model name for the provider.

        Raises:
            ValueError: If name or api_key is empty.
            OSError: If configuration cannot be saved.
        """
        if not name or not name.strip():
            raise ValueError("Provider name cannot be empty")
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")

        if "providers" not in self.config:
            self.config["providers"] = {}

        provider_config = {
            "api_key": api_key.strip()
        }

        if model:
            provider_config["model"] = model.strip()

        self.config["providers"][name.strip()] = provider_config
        self.save_config()

    def get_providers(self) -> Dict[str, Dict[str, str]]:
        """Get all configured providers.

        Returns:
            Dictionary mapping provider names to their configurations.
            Each provider configuration contains 'api_key' and optionally 'model'.
        """
        return self.config.get("providers", {})

    def grant_permissions(self, granted: bool = True, exclude_paths: Optional[List[str]] = None) -> None:
        """Update privacy permissions settings.

        Args:
            granted: Whether permissions are granted for file scanning.
            exclude_paths: Optional list of paths to exclude from scanning.

        Raises:
            OSError: If configuration cannot be saved.
        """
        if "privacy" not in self.config:
            self.config["privacy"] = {
                "permissions_granted": False,
                "exclude_paths": []
            }

        self.config["privacy"]["permissions_granted"] = granted

        if exclude_paths is not None:
            self.config["privacy"]["exclude_paths"] = exclude_paths

        self.save_config()

    def get_scanning_config(self) -> Dict[str, Any]:
        """Get scanning configuration settings.

        Returns:
            Dictionary containing scanning configuration.
        """
        return self.config.get("scanning", self.get_default_config()["scanning"])

    def get_knowledge_base_config(self) -> Dict[str, str]:
        """Get knowledge base configuration settings.

        Returns:
            Dictionary containing knowledge base configuration.
        """
        return self.config.get("knowledge_base", self.get_default_config()["knowledge_base"])

    def get_privacy_config(self) -> Dict[str, Any]:
        """Get privacy configuration settings.

        Returns:
            Dictionary containing privacy configuration.
        """
        return self.config.get("privacy", self.get_default_config()["privacy"])

    def is_permissions_granted(self) -> bool:
        """Check if file scanning permissions are granted.

        Returns:
            True if permissions are granted, False otherwise.
        """
        privacy_config = self.get_privacy_config()
        return privacy_config.get("permissions_granted", False)

    def get_provider(self, name: str) -> Optional[Dict[str, str]]:
        """Get configuration for a specific provider.

        Args:
            name: Provider name to retrieve.

        Returns:
            Provider configuration dictionary or None if not found.
        """
        providers = self.get_providers()
        return providers.get(name)

    def remove_provider(self, name: str) -> bool:
        """Remove a provider from configuration.

        Args:
            name: Provider name to remove.

        Returns:
            True if provider was removed, False if it didn't exist.

        Raises:
            OSError: If configuration cannot be saved.
        """
        if "providers" not in self.config:
            return False

        if name in self.config["providers"]:
            del self.config["providers"][name]
            self.save_config()
            return True

        return False

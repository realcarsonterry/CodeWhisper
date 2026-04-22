"""Scanning engine for codebase analysis.

This module provides a multi-threaded scanning engine that analyzes codebases
using AI providers. It consists of:

- FileDiscovery: Discovers files to scan based on configuration rules
- TaskQueue: Thread-safe queue for distributing tasks
- SubAgent: Worker agents that analyze files using AI providers
- MasterAgent: Coordinates the entire scanning process

Example usage:
    from codewhisper.scanner import MasterAgent
    from codewhisper.providers import ClaudeProvider

    # Initialize providers
    provider = ClaudeProvider(api_key="your-key", model="claude-opus-4-20250514")

    # Create master agent
    master = MasterAgent(
        providers=[provider],
        exclude_dirs=["node_modules", ".git"],
        exclude_files=["*.pyc", "*.log"]
    )

    # Scan directory
    results = master.scan_directory("/path/to/project", max_agents=10)

    # Build knowledge graph
    graph = master.build_knowledge_graph()
"""

from codewhisper.scanner.file_discovery import FileDiscovery
from codewhisper.scanner.task_queue import TaskQueue
from codewhisper.scanner.sub_agent import SubAgent
from codewhisper.scanner.master_agent import MasterAgent

__all__ = [
    'FileDiscovery',
    'TaskQueue',
    'SubAgent',
    'MasterAgent',
]

"""Sub-agent module for parallel file analysis."""

import asyncio
from pathlib import Path
from typing import Dict, Any, Optional
from threading import Thread

from codewhisper.providers.base import AIProvider
from codewhisper.scanner.task_queue import TaskQueue


class SubAgent:
    """Sub-agent that processes file analysis tasks using an AI provider.

    Each sub-agent runs in its own thread and processes tasks from a shared
    task queue, analyzing files using the assigned AI provider.
    """

    def __init__(
        self,
        agent_id: int,
        provider: AIProvider,
        task_queue: TaskQueue,
        results: Dict[str, Any]
    ):
        """Initialize the sub-agent.

        Args:
            agent_id: Unique identifier for this agent
            provider: AI provider instance to use for analysis
            task_queue: Shared task queue to pull tasks from
            results: Shared dictionary to store analysis results
        """
        self.agent_id = agent_id
        self.provider = provider
        self.task_queue = task_queue
        self.results = results
        self._thread: Optional[Thread] = None
        self._running = False

    def run(self) -> None:
        """Run the agent in the current thread.

        This method processes tasks from the queue until the queue is empty.
        It should be called from within a thread pool executor.
        """
        self._running = True

        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            while self._running:
                # Get task with short timeout to allow checking _running flag
                task = self.task_queue.get_task(timeout=1.0)

                if task is None:
                    # No more tasks available
                    break

                try:
                    # Process the task
                    result = loop.run_until_complete(self.process_task(task))

                    # Store result
                    if result:
                        self.results[task] = result

                    # Mark task as completed
                    self.task_queue.mark_completed()

                except Exception as e:
                    # Log error but continue processing
                    self.results[task] = {
                        "error": str(e),
                        "agent_id": self.agent_id,
                        "status": "failed"
                    }
                    self.task_queue.mark_completed()
        finally:
            loop.close()

    async def process_task(self, task: str) -> Optional[Dict[str, Any]]:
        """Process a single file analysis task.

        Args:
            task: File path to analyze

        Returns:
            Dictionary containing analysis results or None if analysis failed
        """
        try:
            file_path = task
            analysis = await self.analyze_file(file_path)

            return {
                "file_path": file_path,
                "analysis": analysis,
                "agent_id": self.agent_id,
                "status": "success"
            }
        except Exception as e:
            return {
                "file_path": task,
                "error": str(e),
                "agent_id": self.agent_id,
                "status": "failed"
            }

    async def analyze_file(self, file_path: str) -> str:
        """Analyze a file using the AI provider.

        Args:
            file_path: Path to the file to analyze

        Returns:
            Analysis result from the AI provider

        Raises:
            OSError: If file cannot be read
            Exception: If AI provider call fails
        """
        # Read file content
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            raise OSError(f"Failed to read file {file_path}: {e}")

        # Prepare analysis prompt - SIMPLIFIED for speed
        file_name = Path(file_path).name
        file_ext = Path(file_path).suffix

        # Use a much shorter, faster prompt
        system_prompt = "You are a code analyzer. Provide a brief 2-3 sentence summary."

        user_message = f"""File: {file_name}

```
{content[:3000]}
```

Summarize in 2-3 sentences: What does this file do?"""

        # Call AI provider with retry logic for rate limits
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(max_retries):
            try:
                analysis = await self.provider.send_message(
                    message=user_message,
                    system_prompt=system_prompt,
                    temperature=0.1,  # Lower for faster, more deterministic responses
                    max_tokens=200    # Much smaller for speed
                )
                return analysis
            except Exception as e:
                error_msg = str(e).lower()
                # Check if it's a rate limit error
                if 'rate' in error_msg or 'limit' in error_msg or '429' in error_msg:
                    if attempt < max_retries - 1:
                        # Exponential backoff
                        wait_time = retry_delay * (2 ** attempt)
                        await asyncio.sleep(wait_time)
                        continue
                raise Exception(f"AI provider analysis failed: {e}")

    def stop(self) -> None:
        """Stop the agent gracefully."""
        self._running = False

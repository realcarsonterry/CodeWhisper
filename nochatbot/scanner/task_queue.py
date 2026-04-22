"""Thread-safe task queue for the scanning engine."""

import queue
from typing import Any, Optional
from threading import Lock


class TaskQueue:
    """Thread-safe task queue for managing file scanning tasks.

    This class provides a thread-safe queue implementation for distributing
    file analysis tasks across multiple sub-agents.
    """

    def __init__(self):
        """Initialize the task queue."""
        self._queue: queue.Queue = queue.Queue()
        self._lock: Lock = Lock()
        self._total_tasks: int = 0
        self._completed_tasks: int = 0

    def add_task(self, task: Any) -> None:
        """Add a task to the queue.

        Args:
            task: Task object to add (typically a file path or task dictionary)
        """
        with self._lock:
            self._queue.put(task)
            self._total_tasks += 1

    def get_task(self, timeout: Optional[float] = None) -> Optional[Any]:
        """Get a task from the queue.

        Args:
            timeout: Optional timeout in seconds to wait for a task.
                    If None, blocks indefinitely. If 0, returns immediately.

        Returns:
            Task object if available, None if queue is empty and timeout occurred

        Raises:
            queue.Empty: If timeout is 0 and queue is empty
        """
        try:
            if timeout == 0:
                return self._queue.get_nowait()
            else:
                return self._queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def mark_completed(self) -> None:
        """Mark a task as completed.

        This should be called after successfully processing a task.
        """
        with self._lock:
            self._completed_tasks += 1
            self._queue.task_done()

    def is_empty(self) -> bool:
        """Check if the queue is empty.

        Returns:
            True if the queue has no pending tasks, False otherwise
        """
        return self._queue.empty()

    def size(self) -> int:
        """Get the current number of pending tasks in the queue.

        Returns:
            Number of tasks waiting to be processed
        """
        return self._queue.qsize()

    def get_progress(self) -> tuple[int, int]:
        """Get the current progress of task processing.

        Returns:
            Tuple of (completed_tasks, total_tasks)
        """
        with self._lock:
            return (self._completed_tasks, self._total_tasks)

    def wait_completion(self) -> None:
        """Block until all tasks have been processed.

        This method blocks until all tasks that have been added to the queue
        have been processed and marked as done via mark_completed().
        """
        self._queue.join()

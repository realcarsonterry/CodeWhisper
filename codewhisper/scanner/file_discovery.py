"""File discovery module for scanning engine."""

import os
from pathlib import Path
from typing import List, Set
import fnmatch


class FileDiscovery:
    """Discovers files in a directory tree based on configuration rules.

    This class handles file system traversal and filtering based on
    exclude patterns for directories and files, as well as file size limits.
    """

    def __init__(
        self,
        exclude_dirs: List[str] = None,
        exclude_files: List[str] = None,
        max_file_size_mb: float = 10.0
    ):
        """Initialize the file discovery engine.

        Args:
            exclude_dirs: List of directory names to exclude from scanning
            exclude_files: List of file patterns to exclude (supports wildcards)
            max_file_size_mb: Maximum file size in MB to include
        """
        self.exclude_dirs: Set[str] = set(exclude_dirs or [])
        self.exclude_files: List[str] = exclude_files or []
        self.max_file_size_bytes: int = int(max_file_size_mb * 1024 * 1024)

    def should_include(self, path: Path) -> bool:
        """Determine if a file should be included in scanning.

        Args:
            path: Path object to check

        Returns:
            True if the file should be included, False otherwise
        """
        # Check if it's a file
        if not path.is_file():
            return False

        # Check file size
        try:
            if path.stat().st_size > self.max_file_size_bytes:
                return False
        except OSError:
            return False

        # Check against exclude patterns
        filename = path.name
        for pattern in self.exclude_files:
            if fnmatch.fnmatch(filename, pattern):
                return False

        return True

    def _should_exclude_dir(self, dir_name: str) -> bool:
        """Check if a directory should be excluded.

        Args:
            dir_name: Name of the directory to check

        Returns:
            True if the directory should be excluded, False otherwise
        """
        return dir_name in self.exclude_dirs

    def discover(self, root_path: str) -> List[str]:
        """Discover all files in the directory tree that should be scanned.

        Args:
            root_path: Root directory path to start discovery from

        Returns:
            List of absolute file paths to scan

        Raises:
            ValueError: If root_path doesn't exist or is not a directory
            OSError: If there are permission issues accessing the directory
        """
        root = Path(root_path).resolve()

        if not root.exists():
            raise ValueError(f"Path does not exist: {root_path}")

        if not root.is_dir():
            raise ValueError(f"Path is not a directory: {root_path}")

        discovered_files: List[str] = []

        try:
            for dirpath, dirnames, filenames in os.walk(root):
                # Filter out excluded directories in-place
                # This prevents os.walk from descending into them
                dirnames[:] = [
                    d for d in dirnames
                    if not self._should_exclude_dir(d)
                ]

                # Check each file
                current_dir = Path(dirpath)
                for filename in filenames:
                    file_path = current_dir / filename
                    if self.should_include(file_path):
                        discovered_files.append(str(file_path))

        except PermissionError as e:
            raise OSError(f"Permission denied accessing directory: {e}")

        return discovered_files

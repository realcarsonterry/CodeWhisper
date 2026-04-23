"""Master agent for coordinating the scanning process."""

import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional
from pathlib import Path

from codewhisper.providers.base import AIProvider
from codewhisper.scanner.file_discovery import FileDiscovery
from codewhisper.scanner.task_queue import TaskQueue
from codewhisper.scanner.sub_agent import SubAgent


class MasterAgent:
    """Master agent that coordinates the entire scanning process.

    The master agent discovers files, distributes tasks to sub-agents,
    and aggregates results into a knowledge graph.
    """

    def __init__(
        self,
        providers: List[AIProvider],
        exclude_dirs: List[str] = None,
        exclude_files: List[str] = None,
        max_file_size_mb: float = 10.0
    ):
        """Initialize the master agent.

        Args:
            providers: List of AI provider instances to use for analysis
            exclude_dirs: List of directory names to exclude from scanning
            exclude_files: List of file patterns to exclude (supports wildcards)
            max_file_size_mb: Maximum file size in MB to include
        """
        if not providers:
            raise ValueError("At least one AI provider must be provided")

        self.providers = providers
        self.file_discovery = FileDiscovery(
            exclude_dirs=exclude_dirs,
            exclude_files=exclude_files,
            max_file_size_mb=max_file_size_mb
        )
        self.results: Dict[str, Any] = {}
        self.knowledge_graph: Dict[str, Any] = {}

    def scan_directory(
        self,
        path: str,
        max_agents: int = 1000,
        show_progress: bool = True
    ) -> Dict[str, Any]:
        """Scan a directory and analyze all files using parallel sub-agents.

        Args:
            path: Root directory path to scan
            max_agents: Maximum number of parallel sub-agents to use (default: 1000)
            show_progress: Whether to display progress information

        Returns:
            Dictionary containing scan results and statistics

        Raises:
            ValueError: If path is invalid
            OSError: If there are permission issues
        """
        if show_progress:
            print(f"Starting directory scan: {path}")
            print(f"Using {len(self.providers)} AI provider(s)")

        # Discover files
        try:
            files = self.file_discovery.discover(path)
        except Exception as e:
            raise ValueError(f"File discovery failed: {e}")

        if not files:
            return {
                "status": "completed",
                "files_scanned": 0,
                "files_analyzed": 0,
                "errors": 0,
                "results": {}
            }

        if show_progress:
            print(f"Discovered {len(files)} files to analyze")

        # Create task queue and populate it
        task_queue = TaskQueue()
        for file_path in files:
            task_queue.add_task(file_path)

        # IMPORTANT: Create one agent per file for maximum parallelism!
        # This is the core of "No Chat Bot" - hundreds/thousands of agents working simultaneously
        # However, limit concurrent API calls to avoid rate limits
        num_agents = min(max_agents, len(files))

        # If user wants more agents than files, use one agent per file
        if num_agents >= len(files):
            num_agents = len(files)
            if show_progress:
                print(f"Creating {num_agents} sub-agents (one per file) for maximum speed...")
        else:
            if show_progress:
                print(f"Creating {num_agents} sub-agents (limited by max_agents parameter)...")

        # Limit concurrent workers to avoid API rate limits
        # Even with 1000 agents, only 20 will call API simultaneously
        concurrent_workers = min(num_agents, 20)

        if show_progress:
            print(f"Using {concurrent_workers} concurrent API workers to respect rate limits...")

        # Create sub-agents with round-robin provider assignment
        sub_agents = []
        for i in range(num_agents):
            provider = self.providers[i % len(self.providers)]
            agent = SubAgent(
                agent_id=i,
                provider=provider,
                task_queue=task_queue,
                results=self.results
            )
            sub_agents.append(agent)

        # Run sub-agents in parallel using ThreadPoolExecutor
        # Use a large thread pool to handle hundreds/thousands of concurrent agents
        with ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
            # Submit all agents
            futures = [executor.submit(agent.run) for agent in sub_agents]

            # Monitor progress
            if show_progress:
                try:
                    import time
                    while True:
                        completed, total = task_queue.get_progress()
                        progress_pct = (completed / total * 100) if total > 0 else 0
                        print(f"\rProgress: {completed}/{total} files ({progress_pct:.1f}%) | {num_agents} agents working", end='', flush=True)

                        # Exit when all futures are done (this is the reliable signal)
                        if all(f.done() for f in futures):
                            break

                        # Small delay to avoid busy waiting
                        time.sleep(0.1)

                    print()  # New line after progress
                except KeyboardInterrupt:
                    print("\nScan interrupted by user")
                    for agent in sub_agents:
                        agent.stop()
                    raise

            # Wait for all agents to complete
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    if show_progress:
                        print(f"\nAgent error: {e}", file=sys.stderr)

        # Calculate statistics
        total_files = len(files)
        successful = sum(1 for r in self.results.values() if r.get("status") == "success")
        errors = sum(1 for r in self.results.values() if r.get("status") == "failed")

        if show_progress:
            print(f"\nScan completed:")
            print(f"  Total files: {total_files}")
            print(f"  Successfully analyzed: {successful}")
            print(f"  Errors: {errors}")
            print(f"  Agents used: {num_agents}")

        return {
            "status": "completed",
            "files_scanned": total_files,
            "files_analyzed": successful,
            "errors": errors,
            "results": self.results
        }

    def build_knowledge_graph(self) -> Dict[str, Any]:
        """Build a simplified knowledge graph from analysis results.

        Returns:
            Dictionary representing the knowledge graph structure
        """
        if not self.results:
            return {
                "nodes": [],
                "edges": [],
                "metadata": {
                    "total_files": 0,
                    "total_nodes": 0,
                    "total_edges": 0
                }
            }

        nodes = []
        edges = []

        # Create nodes for each successfully analyzed file
        for file_path, result in self.results.items():
            if result.get("status") == "success":
                node = {
                    "id": file_path,
                    "type": "file",
                    "name": Path(file_path).name,
                    "path": file_path,
                    "analysis": result.get("analysis", ""),
                    "extension": Path(file_path).suffix
                }
                nodes.append(node)

        # Simple edge creation based on directory structure
        # Limit edges to avoid performance issues with large directories
        file_by_dir: Dict[str, List[str]] = {}
        for file_path in self.results.keys():
            dir_path = str(Path(file_path).parent)
            if dir_path not in file_by_dir:
                file_by_dir[dir_path] = []
            file_by_dir[dir_path].append(file_path)

        # Create edges between files in the same directory
        # Limit to max 10 edges per file to avoid O(n²) explosion
        edge_id = 0
        MAX_EDGES_PER_FILE = 10

        for dir_path, files in file_by_dir.items():
            # Skip edge creation for very large directories
            if len(files) > 100:
                continue

            for i, file1 in enumerate(files):
                edges_created = 0
                for file2 in files[i+1:]:
                    if edges_created >= MAX_EDGES_PER_FILE:
                        break
                    edges.append({
                        "id": edge_id,
                        "source": file1,
                        "target": file2,
                        "type": "same_directory",
                        "weight": 1.0
                    })
                    edge_id += 1
                    edges_created += 1

        self.knowledge_graph = {
            "nodes": nodes,
            "edges": edges,
            "metadata": {
                "total_files": len(self.results),
                "total_nodes": len(nodes),
                "total_edges": len(edges)
            }
        }

        return self.knowledge_graph

    def get_results(self) -> Dict[str, Any]:
        """Get the raw analysis results.

        Returns:
            Dictionary mapping file paths to their analysis results
        """
        return self.results

    def get_knowledge_graph(self) -> Dict[str, Any]:
        """Get the knowledge graph.

        Returns:
            Dictionary representing the knowledge graph structure
        """
        return self.knowledge_graph

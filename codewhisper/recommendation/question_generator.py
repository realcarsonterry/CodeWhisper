"""Question generator for creating intelligent recommendations."""

import json
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class QuestionOption:
    """Represents a single question option."""
    id: str
    text: str
    description: str


@dataclass
class QuestionResult:
    """Result containing question and options."""
    question: str
    options: List[Dict[str, str]]


class QuestionGenerator:
    """Generates intelligent questions based on context.

    This class is responsible for generating 8 high-quality options
    for users to choose from, based on different contexts:
    - First time: Based on project scan results
    - Subsequent: Based on selection history
    - From Chat: Deep understanding of chat content
    """

    def __init__(self, ai_provider):
        """Initialize the question generator.

        Args:
            ai_provider: AI provider instance for generating questions
        """
        self.ai_provider = ai_provider
        self.knowledge_base = []

    async def generate_questions(self, context: Dict[str, Any]) -> QuestionResult:
        """Generate 8 high-quality options based on context.

        Args:
            context: Dictionary containing:
                - type: 'first_time', 'subsequent', or 'from_chat'
                - scan_results: Project scan results (for first_time)
                - selection_history: Previous selections (for subsequent)
                - chat_content: Chat conversation content (for from_chat)
                - knowledge_base: Accumulated knowledge about the project

        Returns:
            QuestionResult with question and 8 options

        Raises:
            ValueError: If context is invalid
            Exception: If AI generation fails
        """
        try:
            # Validate context
            if not context or 'type' not in context:
                raise ValueError("Context must contain 'type' field")

            # Update knowledge base if provided
            if 'knowledge_base' in context:
                self.knowledge_base = context['knowledge_base']

            # Build prompt based on context type
            prompt = self._build_prompt(context)

            # Call AI to generate questions
            logger.info(f"Generating questions for context type: {context['type']}")
            response = await self.ai_provider.send_message(
                message=prompt,
                system_prompt=self._get_system_prompt(),
                temperature=0.7,
                max_tokens=2048
            )

            # Parse AI response
            result = self._parse_response(response)

            # Ensure we have exactly 8 options
            result = self._ensure_8_options(result)

            logger.info(f"Successfully generated question with {len(result.options)} options")
            return result

        except ValueError as e:
            logger.error(f"Invalid context: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to generate questions: {e}")
            # DO NOT return default options - raise the error so caller can handle it
            raise RuntimeError(f"Question generation failed: {e}") from e

    def _build_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt based on context type.

        Args:
            context: Context dictionary

        Returns:
            Formatted prompt string
        """
        context_type = context['type']

        if context_type == 'first_time':
            return self._build_first_time_prompt(context)
        elif context_type == 'subsequent':
            return self._build_subsequent_prompt(context)
        elif context_type == 'from_chat':
            return self._build_from_chat_prompt(context)
        else:
            raise ValueError(f"Unknown context type: {context_type}")

    def _build_first_time_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt for first-time interaction based on project scan.

        Args:
            context: Must contain 'scan_results'

        Returns:
            Formatted prompt
        """
        scan_results = context.get('scan_results', {})

        # Summarize scan results
        project_summary = self._summarize_scan_results(scan_results)

        prompt = f"""Based on the following project scan results, generate a guiding question and 8 high-quality options to help users deeply understand the project.

Project scan results:
{project_summary}

Please generate:
1. An open-ended guiding question to help users choose their exploration direction
2. 8 specific options, each should:
   - Target different aspects of the project (architecture, features, tech stack, code quality, etc.)
   - Have clear exploration value
   - Guide users to deeply understand the project
   - Be clearly described so users know what information they'll get

Return in JSON format:
{{
    "question": "What aspect of this project would you like to explore?",
    "options": [
        {{"id": "1", "text": "Option title", "description": "Detailed option description"}},
        ...8 options total
    ]
}}"""

        return prompt

    def _build_subsequent_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt for subsequent interactions based on selection history.

        Args:
            context: Must contain 'selection_history'

        Returns:
            Formatted prompt
        """
        selection_history = context.get('selection_history', [])

        # Summarize previous selections
        history_summary = self._summarize_selection_history(selection_history)

        # Summarize knowledge base
        kb_summary = self._summarize_knowledge_base()

        prompt = f"""Based on the user's previous selection history and accumulated project knowledge, generate the next guiding question and 8 options.

User selection history:
{history_summary}

Known project information:
{kb_summary}

Please generate:
1. A guiding question that continues from the previous conversation to help users explore further
2. 8 new options that should:
   - Provide deeper exploration directions based on what the user already knows
   - Avoid repeating previously explored content
   - Offer different analytical perspectives
   - Maintain coherence for natural conversation flow

Return in JSON format:
{{
    "question": "Based on your previous choice, what would you like to explore next?",
    "options": [
        {{"id": "1", "text": "Option title", "description": "Detailed option description"}},
        ...8 options total
    ]
}}"""

        return prompt

    def _build_from_chat_prompt(self, context: Dict[str, Any]) -> str:
        """Build prompt when switching back from Chat mode.

        Args:
            context: Must contain 'chat_content'

        Returns:
            Formatted prompt
        """
        chat_content = context.get('chat_content', [])

        # Summarize chat conversation
        chat_summary = self._summarize_chat_content(chat_content)

        # Summarize knowledge base
        kb_summary = self._summarize_knowledge_base()

        prompt = f"""User just switched back from free chat mode. Based on the conversation content and project knowledge, generate a guiding question and 8 options.

Conversation summary:
{chat_summary}

Known project information:
{kb_summary}

Please generate:
1. A guiding question based on the conversation content to help users continue exploring related topics
2. 8 options that should:
   - Deeply understand the issues and interests the user focused on in the conversation
   - Provide in-depth exploration directions related to the conversation topic
   - Combine with actual project conditions to give specific and feasible analysis perspectives
   - Help users transition from abstract discussion in conversation to specific code analysis

Return in JSON format:
{{
    "question": "Based on our conversation, what aspect would you like to explore in depth?",
    "options": [
        {{"id": "1", "text": "Option title", "description": "Detailed option description"}},
        ...8 options total
    ]
}}"""

        return prompt

    def _summarize_scan_results(self, scan_results: Dict[str, Any]) -> str:
        """Summarize project scan results.

        Args:
            scan_results: Raw scan results

        Returns:
            Formatted summary string
        """
        if not scan_results:
            return "No scan results available"

        summary_parts = []

        # File statistics
        if 'file_count' in scan_results:
            summary_parts.append(f"File count: {scan_results['file_count']}")

        # Language distribution
        if 'languages' in scan_results:
            langs = ', '.join([f"{k}: {v}" for k, v in scan_results['languages'].items()])
            summary_parts.append(f"Programming languages: {langs}")

        # Project structure
        if 'structure' in scan_results:
            summary_parts.append(f"Project structure: {scan_results['structure']}")

        # Dependencies
        if 'dependencies' in scan_results:
            deps = ', '.join(scan_results['dependencies'][:10])  # First 10
            summary_parts.append(f"Main dependencies: {deps}")

        # Key files
        if 'key_files' in scan_results:
            files = ', '.join(scan_results['key_files'][:10])
            summary_parts.append(f"Key files: {files}")

        return '\n'.join(summary_parts) if summary_parts else "Project scan completed"

    def _summarize_selection_history(self, history: List[Dict[str, Any]]) -> str:
        """Summarize user's selection history.

        Args:
            history: List of previous selections

        Returns:
            Formatted summary string
        """
        if not history:
            return "No selection history available"

        summary_parts = []
        for i, item in enumerate(history[-5:], 1):  # Last 5 selections
            question = item.get('question', 'Unknown question')
            selected = item.get('selected_option', {})
            text = selected.get('text', 'Unknown option')
            summary_parts.append(f"{i}. {question}\n   Selected: {text}")

        return '\n'.join(summary_parts)

    def _summarize_chat_content(self, chat_content: List[Dict[str, str]]) -> str:
        """Summarize chat conversation content.

        Args:
            chat_content: List of chat messages

        Returns:
            Formatted summary string
        """
        if not chat_content:
            return "No conversation content available"

        # Get last 10 messages
        recent_messages = chat_content[-10:]

        summary_parts = []
        for msg in recent_messages:
            role = msg.get('role', 'unknown')
            content = msg.get('content', '')
            # Truncate long messages
            if len(content) > 100:
                content = content[:100] + "..."
            summary_parts.append(f"{role}: {content}")

        return '\n'.join(summary_parts)

    def _summarize_knowledge_base(self) -> str:
        """Summarize accumulated knowledge base.

        Returns:
            Formatted summary string
        """
        if not self.knowledge_base:
            return "No accumulated project knowledge available"

        # Take last 5 knowledge items
        recent_knowledge = self.knowledge_base[-5:]

        summary_parts = []
        for i, item in enumerate(recent_knowledge, 1):
            if isinstance(item, dict):
                topic = item.get('topic', 'Unknown topic')
                summary = item.get('summary', 'No summary')
                summary_parts.append(f"{i}. {topic}: {summary}")
            else:
                summary_parts.append(f"{i}. {str(item)}")

        return '\n'.join(summary_parts)

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI.

        Returns:
            System prompt string
        """
        return """You are a professional code analysis assistant, skilled at helping developers understand and explore codebases.

Your task is to generate guiding questions and options to help users:
1. Systematically understand project structure and functionality
2. Deeply explore technical details of interest
3. Discover key patterns and design decisions in the code
4. Understand the project's tech stack and architectural choices

When generating options, pay attention to:
- Each option should have clear exploration value
- Options should cover different dimensions and levels
- Descriptions should be clear and specific, letting users know what they'll get
- Maintain a professional but friendly tone

Must strictly return results in JSON format."""

    def _parse_response(self, response: str) -> QuestionResult:
        """Parse AI response into QuestionResult.

        Args:
            response: Raw AI response string

        Returns:
            Parsed QuestionResult

        Raises:
            ValueError: If response format is invalid
        """
        try:
            # Try to find JSON in response
            response = response.strip()

            # Log the raw response for debugging
            logger.debug(f"Raw response length: {len(response)}")
            logger.debug(f"Raw response preview: {response[:500]}")

            if not response:
                raise ValueError("Empty response from AI provider")

            # Remove markdown code blocks if present
            if response.startswith('```'):
                lines = response.split('\n')
                # Remove first line (```json or ```) and last line (```)
                if len(lines) > 2:
                    response = '\n'.join(lines[1:-1])
                else:
                    raise ValueError("Invalid markdown code block format")

            # Try to extract JSON if there's extra text
            # Look for { ... } pattern
            import re
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                response = json_match.group(0)
            else:
                raise ValueError("No JSON object found in response")

            # Parse JSON
            data = json.loads(response)

            # Validate structure
            if 'question' not in data or 'options' not in data:
                raise ValueError("Response missing required fields: 'question' or 'options'")

            if not isinstance(data['options'], list):
                raise ValueError("Options must be a list")

            if len(data['options']) == 0:
                raise ValueError("Options list is empty")

            # Validate each option has required fields
            for i, opt in enumerate(data['options']):
                if not isinstance(opt, dict):
                    raise ValueError(f"Option {i} is not a dictionary")
                if 'id' not in opt or 'text' not in opt or 'description' not in opt:
                    raise ValueError(f"Option {i} missing required fields")

            # Convert to QuestionResult
            return QuestionResult(
                question=data['question'],
                options=data['options']
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Response was: {response[:1000]}")
            raise ValueError(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
            logger.error(f"Response preview: {response[:500] if response else 'EMPTY'}")
            raise ValueError(f"Failed to parse response: {e}")

    def _ensure_8_options(self, result: QuestionResult) -> QuestionResult:
        """Ensure result has exactly 8 options.

        Args:
            result: QuestionResult to validate

        Returns:
            QuestionResult with exactly 8 options
        """
        options = result.options

        # If we have exactly 8, return as is
        if len(options) == 8:
            return result

        # If we have more than 8, take first 8
        if len(options) > 8:
            logger.warning(f"Got {len(options)} options, truncating to 8")
            return QuestionResult(
                question=result.question,
                options=options[:8]
            )

        # If we have less than 8, pad with generic options
        logger.warning(f"Got only {len(options)} options, padding to 8")

        generic_options = [
            {
                "id": str(len(options) + 1),
                "text": "View overall architecture",
                "description": "Understand the overall structure and organization of the project"
            },
            {
                "id": str(len(options) + 2),
                "text": "Analyze core functionality",
                "description": "Deep dive into how the core features are implemented"
            },
            {
                "id": str(len(options) + 3),
                "text": "Explore tech stack",
                "description": "Understand the technology stack and reasons for choices"
            },
            {
                "id": str(len(options) + 4),
                "text": "Check code quality",
                "description": "Analyze code quality, maintainability and best practices"
            },
            {
                "id": str(len(options) + 5),
                "text": "Understand dependencies",
                "description": "View project dependencies and module coupling"
            },
            {
                "id": str(len(options) + 6),
                "text": "View test coverage",
                "description": "Understand testing strategy and coverage"
            },
            {
                "id": str(len(options) + 7),
                "text": "Analyze performance",
                "description": "Explore performance optimizations and considerations"
            },
            {
                "id": str(len(options) + 8),
                "text": "Other aspects",
                "description": "Explore other interesting aspects of the project"
            }
        ]

        # Add generic options until we have 8
        needed = 8 - len(options)
        for i in range(needed):
            options.append(generic_options[i])

        return QuestionResult(
            question=result.question,
            options=options
        )

    def _get_default_options(self) -> QuestionResult:
        """Get default options when generation fails.

        Returns:
            QuestionResult with default question and 8 options
        """
        logger.info("Using default options as fallback")

        return QuestionResult(
            question="Which aspect of this project would you like to explore?",
            options=[
                {
                    "id": "1",
                    "text": "Overall architecture",
                    "description": "Understand the overall structure, module division and organization"
                },
                {
                    "id": "2",
                    "text": "Core functionality",
                    "description": "Deep dive into how the core features are implemented"
                },
                {
                    "id": "3",
                    "text": "Tech stack analysis",
                    "description": "Understand the technology stack, frameworks and tools used"
                },
                {
                    "id": "4",
                    "text": "Code quality assessment",
                    "description": "Analyze code quality, maintainability and best practices"
                },
                {
                    "id": "5",
                    "text": "Dependency graph",
                    "description": "View project dependencies and module coupling"
                },
                {
                    "id": "6",
                    "text": "Testing strategy",
                    "description": "Understand testing strategy, coverage and methods"
                },
                {
                    "id": "7",
                    "text": "Performance optimization",
                    "description": "Explore performance optimization strategies and considerations"
                },
                {
                    "id": "8",
                    "text": "Configuration and deployment",
                    "description": "Understand configuration management and deployment process"
                }
            ]
        )

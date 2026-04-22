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

    def generate_questions(self, context: Dict[str, Any]) -> QuestionResult:
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
            response = self.ai_provider.send_message(
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
            # Return default options as fallback
            return self._get_default_options()

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

        prompt = f"""基于以下项目扫描结果，生成一个引导性问题和8个高质量选项，帮助用户深入了解项目。

项目扫描结果：
{project_summary}

请生成：
1. 一个开放性的引导问题，帮助用户选择他们想了解的方向
2. 8个具体的选项，每个选项应该：
   - 针对项目的不同方面（架构、功能、技术栈、代码质量等）
   - 具有明确的探索价值
   - 能够引导用户深入了解项目
   - 描述清晰，让用户知道选择后会得到什么信息

请以JSON格式返回，格式如下：
{{
    "question": "你想了解这个项目的哪个方面？",
    "options": [
        {{"id": "1", "text": "选项标题", "description": "选项详细描述"}},
        ...共8个选项
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

        prompt = f"""基于用户之前的选择历史和已积累的项目知识，生成下一个引导性问题和8个选项。

用户选择历史：
{history_summary}

已知项目信息：
{kb_summary}

请生成：
1. 一个承接之前对话的引导问题，帮助用户继续深入探索
2. 8个新的选项，应该：
   - 基于用户已经了解的内容，提供更深入的探索方向
   - 避免重复之前已经探索过的内容
   - 提供不同维度的分析角度
   - 保持连贯性，让对话自然流畅

请以JSON格式返回，格式如下：
{{
    "question": "基于你刚才的选择，接下来想了解什么？",
    "options": [
        {{"id": "1", "text": "选项标题", "description": "选项详细描述"}},
        ...共8个选项
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

        prompt = f"""用户刚从自由对话模式切换回来。基于对话内容和项目知识，生成引导性问题和8个选项。

对话内容摘要：
{chat_summary}

已知项目信息：
{kb_summary}

请生成：
1. 一个基于对话内容的引导问题，帮助用户继续探索相关主题
2. 8个选项，应该：
   - 深度理解对话中用户关注的问题和兴趣点
   - 提供与对话主题相关的深入探索方向
   - 结合项目实际情况，给出具体可行的分析角度
   - 帮助用户从对话中的抽象讨论转向具体的代码分析

请以JSON格式返回，格式如下：
{{
    "question": "基于刚才的对话，你想深入了解哪个方面？",
    "options": [
        {{"id": "1", "text": "选项标题", "description": "选项详细描述"}},
        ...共8个选项
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
            return "暂无扫描结果"

        summary_parts = []

        # File statistics
        if 'file_count' in scan_results:
            summary_parts.append(f"文件数量: {scan_results['file_count']}")

        # Language distribution
        if 'languages' in scan_results:
            langs = ', '.join([f"{k}: {v}" for k, v in scan_results['languages'].items()])
            summary_parts.append(f"编程语言: {langs}")

        # Project structure
        if 'structure' in scan_results:
            summary_parts.append(f"项目结构: {scan_results['structure']}")

        # Dependencies
        if 'dependencies' in scan_results:
            deps = ', '.join(scan_results['dependencies'][:10])  # First 10
            summary_parts.append(f"主要依赖: {deps}")

        # Key files
        if 'key_files' in scan_results:
            files = ', '.join(scan_results['key_files'][:10])
            summary_parts.append(f"关键文件: {files}")

        return '\n'.join(summary_parts) if summary_parts else "项目扫描完成"

    def _summarize_selection_history(self, history: List[Dict[str, Any]]) -> str:
        """Summarize user's selection history.

        Args:
            history: List of previous selections

        Returns:
            Formatted summary string
        """
        if not history:
            return "暂无选择历史"

        summary_parts = []
        for i, item in enumerate(history[-5:], 1):  # Last 5 selections
            question = item.get('question', '未知问题')
            selected = item.get('selected_option', {})
            text = selected.get('text', '未知选项')
            summary_parts.append(f"{i}. {question}\n   选择: {text}")

        return '\n'.join(summary_parts)

    def _summarize_chat_content(self, chat_content: List[Dict[str, str]]) -> str:
        """Summarize chat conversation content.

        Args:
            chat_content: List of chat messages

        Returns:
            Formatted summary string
        """
        if not chat_content:
            return "暂无对话内容"

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
            return "暂无积累的项目知识"

        # Take last 5 knowledge items
        recent_knowledge = self.knowledge_base[-5:]

        summary_parts = []
        for i, item in enumerate(recent_knowledge, 1):
            if isinstance(item, dict):
                topic = item.get('topic', '未知主题')
                summary = item.get('summary', '无摘要')
                summary_parts.append(f"{i}. {topic}: {summary}")
            else:
                summary_parts.append(f"{i}. {str(item)}")

        return '\n'.join(summary_parts)

    def _get_system_prompt(self) -> str:
        """Get system prompt for AI.

        Returns:
            System prompt string
        """
        return """你是一个专业的代码分析助手，擅长帮助开发者理解和探索代码库。

你的任务是生成引导性问题和选项，帮助用户：
1. 系统性地了解项目结构和功能
2. 深入探索感兴趣的技术细节
3. 发现代码中的关键模式和设计决策
4. 理解项目的技术栈和架构选择

生成选项时要注意：
- 每个选项都应该有明确的探索价值
- 选项之间应该覆盖不同的维度和层次
- 描述要清晰具体，让用户知道会得到什么
- 保持专业但友好的语气

必须严格按照JSON格式返回结果。"""

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

            # Remove markdown code blocks if present
            if response.startswith('```'):
                lines = response.split('\n')
                response = '\n'.join(lines[1:-1])

            # Parse JSON
            data = json.loads(response)

            # Validate structure
            if 'question' not in data or 'options' not in data:
                raise ValueError("Response missing required fields")

            if not isinstance(data['options'], list):
                raise ValueError("Options must be a list")

            # Convert to QuestionResult
            return QuestionResult(
                question=data['question'],
                options=data['options']
            )

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.debug(f"Response was: {response}")
            raise ValueError(f"Invalid JSON response: {e}")
        except Exception as e:
            logger.error(f"Failed to parse response: {e}")
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
                "text": "查看项目整体架构",
                "description": "了解项目的整体结构和组织方式"
            },
            {
                "id": str(len(options) + 2),
                "text": "分析核心功能实现",
                "description": "深入了解项目的核心功能是如何实现的"
            },
            {
                "id": str(len(options) + 3),
                "text": "探索技术栈选择",
                "description": "了解项目使用的技术栈及其选择原因"
            },
            {
                "id": str(len(options) + 4),
                "text": "检查代码质量",
                "description": "分析代码的质量、可维护性和最佳实践"
            },
            {
                "id": str(len(options) + 5),
                "text": "了解依赖关系",
                "description": "查看项目的依赖关系和模块间的耦合"
            },
            {
                "id": str(len(options) + 6),
                "text": "查看测试覆盖",
                "description": "了解项目的测试策略和覆盖情况"
            },
            {
                "id": str(len(options) + 7),
                "text": "分析性能考虑",
                "description": "探索项目中的性能优化和考虑"
            },
            {
                "id": str(len(options) + 8),
                "text": "其他方面",
                "description": "探索项目的其他有趣方面"
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
            question="你想了解这个项目的哪个方面？",
            options=[
                {
                    "id": "1",
                    "text": "项目整体架构",
                    "description": "了解项目的整体结构、模块划分和组织方式"
                },
                {
                    "id": "2",
                    "text": "核心功能实现",
                    "description": "深入了解项目的核心功能是如何实现的"
                },
                {
                    "id": "3",
                    "text": "技术栈分析",
                    "description": "了解项目使用的技术栈、框架和工具"
                },
                {
                    "id": "4",
                    "text": "代码质量评估",
                    "description": "分析代码的质量、可维护性和最佳实践应用"
                },
                {
                    "id": "5",
                    "text": "依赖关系图",
                    "description": "查看项目的依赖关系和模块间的耦合情况"
                },
                {
                    "id": "6",
                    "text": "测试策略",
                    "description": "了解项目的测试策略、覆盖率和测试方法"
                },
                {
                    "id": "7",
                    "text": "性能优化",
                    "description": "探索项目中的性能优化策略和考虑"
                },
                {
                    "id": "8",
                    "text": "配置和部署",
                    "description": "了解项目的配置管理和部署流程"
                }
            ]
        )

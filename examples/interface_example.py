"""Example usage of InteractiveInterface.

This example demonstrates how to use the InteractiveInterface class
to create an interactive session with No Chat Bot.
"""

from nochatbot.interaction import InteractiveInterface
from nochatbot.providers.base import AIProvider


# Mock AI Provider for demonstration
class MockAIProvider(AIProvider):
    """Mock AI provider for testing purposes."""

    async def send_message(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock send_message implementation."""
        # Return a JSON response for question generation
        if "生成" in str(message) or "generate" in str(message).lower():
            return """{
                "question": "你想了解这个项目的哪个方面？",
                "options": [
                    {"id": "1", "text": "项目整体架构", "description": "了解项目的整体结构和组织方式"},
                    {"id": "2", "text": "核心功能实现", "description": "深入了解核心功能的实现细节"},
                    {"id": "3", "text": "技术栈分析", "description": "了解项目使用的技术栈和工具"},
                    {"id": "4", "text": "代码质量评估", "description": "分析代码质量和最佳实践"},
                    {"id": "5", "text": "依赖关系图", "description": "查看模块间的依赖关系"},
                    {"id": "6", "text": "测试策略", "description": "了解测试覆盖和测试方法"},
                    {"id": "7", "text": "性能优化", "description": "探索性能优化策略"},
                    {"id": "8", "text": "配置和部署", "description": "了解配置管理和部署流程"}
                ]
            }"""

        # Return a chat response
        return f"This is a mock response to your message. In a real implementation, this would be an intelligent response based on your selection history and the conversation context."

    async def stream_response(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock stream_response implementation."""
        response = await self.send_message(message, system_prompt, temperature, max_tokens, **kwargs)

        # Simulate streaming by yielding chunks
        chunk_size = 20
        for i in range(0, len(response), chunk_size):
            yield response[i:i+chunk_size]

    def get_cost_per_token(self):
        """Mock cost calculation."""
        return {"input": 0.00001, "output": 0.00003}


def main():
    """Run the interactive interface example."""

    # Initialize AI provider
    ai_provider = MockAIProvider(api_key="mock-key", model="mock-model")

    # Project information (optional)
    project_info = {
        "project_name": "No Chat Bot",
        "project_type": "Python CLI Application",
        "tech_stack": "Python, Click, Anthropic API",
        "scan_results": {
            "file_count": 25,
            "languages": {
                "Python": 20,
                "Markdown": 3,
                "YAML": 2
            },
            "structure": "Python package with CLI interface",
            "dependencies": [
                "anthropic", "openai", "click", "python-dotenv",
                "pyyaml", "aiofiles", "gitpython"
            ],
            "key_files": [
                "nochatbot/interaction/interface.py",
                "nochatbot/interaction/chatbot.py",
                "nochatbot/recommendation/question_generator.py",
                "nochatbot/providers/base.py"
            ]
        }
    }

    # Create and start the interactive interface
    interface = InteractiveInterface(
        ai_provider=ai_provider,
        project_info=project_info
    )

    # Start the interactive session
    interface.start()

    # After the session ends, you can access the context
    context = interface.get_context()
    print("\n=== Final Context Summary ===")
    print(context.get_full_context_summary())


if __name__ == "__main__":
    main()

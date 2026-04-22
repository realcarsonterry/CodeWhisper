"""Example usage of QuestionGenerator.

This example demonstrates how to use the QuestionGenerator class
to generate intelligent questions based on different contexts.
"""

from codewhisper.recommendation import QuestionGenerator
from codewhisper.providers.base import AIProvider


# Mock AI Provider for demonstration
class MockAIProvider(AIProvider):
    """Mock AI provider for testing."""

    async def send_message(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock send_message that returns a sample response."""
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

    async def stream_response(self, message, system_prompt=None, temperature=0.7, max_tokens=4096, **kwargs):
        """Mock stream_response."""
        response = await self.send_message(message, system_prompt, temperature, max_tokens, **kwargs)
        yield response

    def get_cost_per_token(self):
        """Mock cost calculation."""
        return {'input': 0.0, 'output': 0.0}


def example_first_time():
    """Example: First time interaction based on project scan."""
    print("=== Example 1: First Time Interaction ===\n")

    # Initialize generator with AI provider
    provider = MockAIProvider(api_key="mock-key", model="mock-model")
    generator = QuestionGenerator(provider)

    # Context for first-time interaction
    context = {
        'type': 'first_time',
        'scan_results': {
            'file_count': 150,
            'languages': {
                'Python': 120,
                'JavaScript': 20,
                'HTML': 10
            },
            'structure': 'Flask web application',
            'dependencies': [
                'flask', 'sqlalchemy', 'pytest', 'requests',
                'jinja2', 'werkzeug', 'click'
            ],
            'key_files': [
                'app.py', 'config.py', 'models.py',
                'routes.py', 'templates/', 'static/'
            ]
        }
    }

    # Generate questions
    result = generator.generate_questions(context)

    # Display results
    print(f"Question: {result.question}\n")
    print("Options:")
    for opt in result.options:
        print(f"  {opt['id']}. {opt['text']}")
        print(f"     {opt['description']}\n")


def example_subsequent():
    """Example: Subsequent interaction based on selection history."""
    print("\n=== Example 2: Subsequent Interaction ===\n")

    provider = MockAIProvider(api_key="mock-key", model="mock-model")
    generator = QuestionGenerator(provider)

    # Context with selection history
    context = {
        'type': 'subsequent',
        'selection_history': [
            {
                'question': '你想了解这个项目的哪个方面？',
                'selected_option': {
                    'id': '1',
                    'text': '项目整体架构',
                    'description': '了解项目的整体结构和组织方式'
                }
            },
            {
                'question': '关于架构，你想深入了解什么？',
                'selected_option': {
                    'id': '2',
                    'text': 'MVC模式实现',
                    'description': '了解项目如何实现MVC架构模式'
                }
            }
        ],
        'knowledge_base': [
            {
                'topic': '项目架构',
                'summary': '项目采用Flask框架，使用MVC架构模式'
            },
            {
                'topic': 'MVC实现',
                'summary': 'Models在models.py中定义，Views使用Jinja2模板，Controllers在routes.py中实现'
            }
        ]
    }

    result = generator.generate_questions(context)

    print(f"Question: {result.question}\n")
    print("Options:")
    for opt in result.options:
        print(f"  {opt['id']}. {opt['text']}")
        print(f"     {opt['description']}\n")


def example_from_chat():
    """Example: Switching back from chat mode."""
    print("\n=== Example 3: From Chat Mode ===\n")

    provider = MockAIProvider(api_key="mock-key", model="mock-model")
    generator = QuestionGenerator(provider)

    # Context with chat history
    context = {
        'type': 'from_chat',
        'chat_content': [
            {
                'role': 'user',
                'content': '这个项目的数据库设计是怎样的？'
            },
            {
                'role': 'assistant',
                'content': '项目使用SQLAlchemy ORM，在models.py中定义了User、Post、Comment等模型...'
            },
            {
                'role': 'user',
                'content': '表之间的关系是如何设计的？'
            },
            {
                'role': 'assistant',
                'content': 'User和Post是一对多关系，Post和Comment也是一对多关系...'
            }
        ],
        'knowledge_base': [
            {
                'topic': '数据库设计',
                'summary': '使用SQLAlchemy ORM，定义了User、Post、Comment等模型'
            },
            {
                'topic': '表关系',
                'summary': 'User-Post一对多，Post-Comment一对多'
            }
        ]
    }

    result = generator.generate_questions(context)

    print(f"Question: {result.question}\n")
    print("Options:")
    for opt in result.options:
        print(f"  {opt['id']}. {opt['text']}")
        print(f"     {opt['description']}\n")


def example_error_handling():
    """Example: Error handling and fallback."""
    print("\n=== Example 4: Error Handling ===\n")

    # Provider that raises an error
    class ErrorProvider(MockAIProvider):
        async def send_message(self, *args, **kwargs):
            raise Exception("API connection failed")

    provider = ErrorProvider(api_key="mock-key", model="mock-model")
    generator = QuestionGenerator(provider)

    context = {
        'type': 'first_time',
        'scan_results': {}
    }

    # Should return default options instead of crashing
    result = generator.generate_questions(context)

    print("When AI fails, default options are returned:\n")
    print(f"Question: {result.question}\n")
    print("Options:")
    for opt in result.options:
        print(f"  {opt['id']}. {opt['text']}")
        print(f"     {opt['description']}\n")


if __name__ == '__main__':
    # Run all examples
    example_first_time()
    example_subsequent()
    example_from_chat()
    example_error_handling()

    print("\n=== Examples Complete ===")

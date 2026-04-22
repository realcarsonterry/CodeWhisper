"""Tests for QuestionGenerator."""

import json
import pytest
from unittest.mock import Mock, AsyncMock
from codewhisper.recommendation import QuestionGenerator, QuestionResult


class TestQuestionGenerator:
    """Test cases for QuestionGenerator."""

    def setup_method(self):
        """Set up test fixtures."""
        self.mock_provider = Mock()
        self.generator = QuestionGenerator(self.mock_provider)

    def test_init(self):
        """Test initialization."""
        assert self.generator.ai_provider == self.mock_provider
        assert self.generator.knowledge_base == []

    def test_generate_questions_first_time(self):
        """Test generating questions for first time."""
        # Mock AI response
        mock_response = json.dumps({
            "question": "你想了解这个项目的哪个方面？",
            "options": [
                {"id": "1", "text": "架构", "description": "了解架构"},
                {"id": "2", "text": "功能", "description": "了解功能"},
                {"id": "3", "text": "技术栈", "description": "了解技术栈"},
                {"id": "4", "text": "代码质量", "description": "了解代码质量"},
                {"id": "5", "text": "依赖", "description": "了解依赖"},
                {"id": "6", "text": "测试", "description": "了解测试"},
                {"id": "7", "text": "性能", "description": "了解性能"},
                {"id": "8", "text": "部署", "description": "了解部署"}
            ]
        })
        self.mock_provider.send_message = Mock(return_value=mock_response)

        context = {
            'type': 'first_time',
            'scan_results': {
                'file_count': 100,
                'languages': {'Python': 80, 'JavaScript': 20}
            }
        }

        result = self.generator.generate_questions(context)

        assert isinstance(result, QuestionResult)
        assert result.question == "你想了解这个项目的哪个方面？"
        assert len(result.options) == 8
        assert all('id' in opt and 'text' in opt and 'description' in opt
                   for opt in result.options)

    def test_generate_questions_subsequent(self):
        """Test generating questions for subsequent interaction."""
        mock_response = json.dumps({
            "question": "接下来想了解什么？",
            "options": [
                {"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                for i in range(1, 9)
            ]
        })
        self.mock_provider.send_message = Mock(return_value=mock_response)

        context = {
            'type': 'subsequent',
            'selection_history': [
                {
                    'question': '之前的问题',
                    'selected_option': {'text': '之前的选择'}
                }
            ]
        }

        result = self.generator.generate_questions(context)

        assert isinstance(result, QuestionResult)
        assert len(result.options) == 8

    def test_generate_questions_from_chat(self):
        """Test generating questions when switching from chat."""
        mock_response = json.dumps({
            "question": "基于对话，你想了解什么？",
            "options": [
                {"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                for i in range(1, 9)
            ]
        })
        self.mock_provider.send_message = Mock(return_value=mock_response)

        context = {
            'type': 'from_chat',
            'chat_content': [
                {'role': 'user', 'content': '用户消息'},
                {'role': 'assistant', 'content': 'AI回复'}
            ]
        }

        result = self.generator.generate_questions(context)

        assert isinstance(result, QuestionResult)
        assert len(result.options) == 8

    def test_invalid_context(self):
        """Test with invalid context."""
        with pytest.raises(ValueError):
            self.generator.generate_questions({})

        with pytest.raises(ValueError):
            self.generator.generate_questions({'type': 'invalid_type'})

    def test_ensure_8_options_truncate(self):
        """Test truncating when more than 8 options."""
        result = QuestionResult(
            question="测试问题",
            options=[{"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                     for i in range(1, 11)]  # 10 options
        )

        ensured = self.generator._ensure_8_options(result)

        assert len(ensured.options) == 8
        assert ensured.options[0]['id'] == "1"
        assert ensured.options[7]['id'] == "8"

    def test_ensure_8_options_pad(self):
        """Test padding when less than 8 options."""
        result = QuestionResult(
            question="测试问题",
            options=[{"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                     for i in range(1, 4)]  # 3 options
        )

        ensured = self.generator._ensure_8_options(result)

        assert len(ensured.options) == 8
        assert ensured.options[0]['id'] == "1"
        assert ensured.options[2]['id'] == "3"
        # Check padded options
        assert ensured.options[3]['id'] == "4"

    def test_parse_response_valid(self):
        """Test parsing valid JSON response."""
        response = json.dumps({
            "question": "测试问题",
            "options": [
                {"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                for i in range(1, 9)
            ]
        })

        result = self.generator._parse_response(response)

        assert isinstance(result, QuestionResult)
        assert result.question == "测试问题"
        assert len(result.options) == 8

    def test_parse_response_with_markdown(self):
        """Test parsing response with markdown code blocks."""
        response = f"""```json
{json.dumps({
    "question": "测试问题",
    "options": [
        {"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
        for i in range(1, 9)
    ]
})}
```"""

        result = self.generator._parse_response(response)

        assert isinstance(result, QuestionResult)
        assert result.question == "测试问题"

    def test_parse_response_invalid(self):
        """Test parsing invalid response."""
        with pytest.raises(ValueError):
            self.generator._parse_response("not json")

        with pytest.raises(ValueError):
            self.generator._parse_response('{"question": "test"}')  # Missing options

    def test_get_default_options(self):
        """Test getting default options."""
        result = self.generator._get_default_options()

        assert isinstance(result, QuestionResult)
        assert len(result.options) == 8
        assert result.question == "你想了解这个项目的哪个方面？"

    def test_fallback_on_error(self):
        """Test fallback to default options on error."""
        self.mock_provider.send_message = Mock(side_effect=Exception("API Error"))

        context = {
            'type': 'first_time',
            'scan_results': {}
        }

        result = self.generator.generate_questions(context)

        # Should return default options instead of raising
        assert isinstance(result, QuestionResult)
        assert len(result.options) == 8

    def test_summarize_scan_results(self):
        """Test summarizing scan results."""
        scan_results = {
            'file_count': 100,
            'languages': {'Python': 80, 'JavaScript': 20},
            'structure': 'monorepo',
            'dependencies': ['flask', 'requests', 'pytest'],
            'key_files': ['app.py', 'config.py']
        }

        summary = self.generator._summarize_scan_results(scan_results)

        assert '100' in summary
        assert 'Python' in summary
        assert 'flask' in summary

    def test_summarize_selection_history(self):
        """Test summarizing selection history."""
        history = [
            {
                'question': '问题1',
                'selected_option': {'text': '选项1'}
            },
            {
                'question': '问题2',
                'selected_option': {'text': '选项2'}
            }
        ]

        summary = self.generator._summarize_selection_history(history)

        assert '问题1' in summary
        assert '选项1' in summary

    def test_summarize_chat_content(self):
        """Test summarizing chat content."""
        chat_content = [
            {'role': 'user', 'content': '用户问题'},
            {'role': 'assistant', 'content': 'AI回答'}
        ]

        summary = self.generator._summarize_chat_content(chat_content)

        assert 'user' in summary
        assert '用户问题' in summary

    def test_knowledge_base_update(self):
        """Test knowledge base update."""
        mock_response = json.dumps({
            "question": "测试",
            "options": [
                {"id": str(i), "text": f"选项{i}", "description": f"描述{i}"}
                for i in range(1, 9)
            ]
        })
        self.mock_provider.send_message = Mock(return_value=mock_response)

        kb = [{'topic': '架构', 'summary': '项目使用MVC架构'}]
        context = {
            'type': 'first_time',
            'scan_results': {},
            'knowledge_base': kb
        }

        self.generator.generate_questions(context)

        assert self.generator.knowledge_base == kb

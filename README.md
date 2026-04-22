# No Chat Bot

An AI-powered codebase analysis and recommendation tool that helps developers understand and explore code repositories through intelligent question-based navigation and contextual chat assistance.

## Features

- **Intelligent Question-Based Navigation**: Explore your codebase through AI-generated questions and options tailored to your project
- **Context-Aware Chat Bot**: Get precise assistance based on your selection history and conversation context
- **Multi-Provider Support**: Works with multiple AI providers (Anthropic Claude, OpenAI, DeepSeek)
- **Smart Code Scanning**: Automatically discovers and analyzes project structure, dependencies, and key files
- **Knowledge Base Integration**: Builds and maintains project knowledge for better recommendations
- **Privacy-Focused**: Configurable permissions and exclusion paths for sensitive data

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/nochatbot.git
cd nochatbot

# Install dependencies
pip install -r requirements.txt

# Or install in development mode
pip install -e .
```

### Configuration

Set up your AI provider API key:

```bash
# For Anthropic Claude
export ANTHROPIC_API_KEY='your-api-key-here'

# For OpenAI
export OPENAI_API_KEY='your-api-key-here'
```

Configure the tool:

```bash
nochatbot config --provider anthropic --api-key YOUR_API_KEY
```

### Basic Usage

Scan a codebase:

```bash
nochatbot scan /path/to/your/project
```

Scan with specific provider:

```bash
nochatbot scan /path/to/your/project --provider openai
```

## Usage

### Command Line Interface

#### Scan Command

Analyze a codebase and generate intelligent recommendations:

```bash
nochatbot scan <path> [OPTIONS]

Options:
  --provider [anthropic|openai]  AI provider to use (default: anthropic)
  --max-agents INTEGER           Maximum number of scanning agents (default: 100)
  --exclude-dir TEXT             Additional directories to exclude
  --exclude-file TEXT            Additional file patterns to exclude
```

#### Config Command

Manage configuration settings:

```bash
# Add a provider
nochatbot config --provider anthropic --api-key YOUR_KEY --model claude-opus-4-20250514

# Grant file scanning permissions
nochatbot config --grant-permissions

# Add exclusion paths
nochatbot config --exclude-path /path/to/sensitive/data
```

### Python API

```python
from nochatbot.config import Config
from nochatbot.providers import ClaudeProvider
from nochatbot.recommendation import QuestionGenerator
from nochatbot.interaction import IntelligentChatBot, ConversationContext

# Initialize configuration
config = Config()

# Set up AI provider
provider = ClaudeProvider(
    api_key=config.get_provider('anthropic')['api_key'],
    model='claude-opus-4-20250514'
)

# Generate questions based on project scan
generator = QuestionGenerator(provider)
result = generator.generate_questions({
    'type': 'first_time',
    'scan_results': {
        'file_count': 150,
        'languages': {'Python': 120, 'JavaScript': 30},
        'key_files': ['main.py', 'config.py']
    }
})

print(result.question)
for option in result.options:
    print(f"- {option['text']}: {option['description']}")

# Use the chat bot
context = ConversationContext()
chatbot = IntelligentChatBot(context, provider)

response = await chatbot.chat("How does the configuration system work?")
print(response)
```

## Configuration

Configuration is stored in `~/.nochatbot/config.json`. See [docs/CONFIGURATION.md](docs/CONFIGURATION.md) for detailed configuration options.

### Configuration Structure

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "your-key",
      "model": "claude-opus-4-20250514"
    }
  },
  "scanning": {
    "max_agents": 100,
    "exclude_dirs": ["node_modules", ".git", "__pycache__"],
    "exclude_files": ["*.pyc", "*.log"],
    "max_file_size_mb": 10
  },
  "knowledge_base": {
    "path": "~/.nochatbot/knowledge",
    "vector_db": "chromadb"
  },
  "privacy": {
    "permissions_granted": false,
    "exclude_paths": []
  }
}
```

## Architecture

No Chat Bot uses a modular architecture with the following key components:

- **Scanner Engine**: Multi-agent system for parallel codebase analysis
- **AI Provider Layer**: Unified interface for multiple AI providers
- **Question Generator**: Creates intelligent, context-aware questions
- **Chat Bot**: Provides contextual assistance based on user history
- **Configuration Manager**: Handles settings and API keys

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed architecture documentation.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Code style and standards
- Development setup
- Testing requirements
- Pull request process

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/yourusername/nochatbot.git
cd nochatbot

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black nochatbot/

# Type checking
mypy nochatbot/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=nochatbot --cov-report=html

# Run specific test file
pytest tests/test_config.py
```

## Requirements

- Python 3.8 or higher
- API key for at least one supported AI provider
- Internet connection for AI API calls

### Dependencies

- `anthropic>=0.40.0` - Anthropic Claude API client
- `openai>=1.0.0` - OpenAI API client
- `click>=8.1.0` - Command-line interface framework
- `python-dotenv>=1.0.0` - Environment variable management
- `pyyaml>=6.0` - YAML configuration support
- `aiofiles>=23.0.0` - Async file operations
- `gitpython>=3.1.0` - Git repository analysis

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check the [documentation](docs/)
- Review existing issues and discussions

## Roadmap

- [ ] Vector database integration for knowledge base
- [ ] Support for more AI providers
- [ ] Web interface
- [ ] IDE plugins (VS Code, JetBrains)
- [ ] Team collaboration features
- [ ] Custom question templates

## Acknowledgments

Built with:
- Anthropic Claude API
- OpenAI API
- Python ecosystem

---

Made with care for developers who want to understand code better.

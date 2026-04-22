# Contributing to No Chat Bot

Thank you for your interest in contributing to No Chat Bot! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Standards](#code-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Project Structure](#project-structure)

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

### Our Standards

- Be respectful and considerate in communication
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Accept responsibility and apologize for mistakes
- Prioritize what's best for the community

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- A GitHub account
- API key for at least one AI provider (Anthropic or OpenAI)

### Finding Issues to Work On

1. Check the [Issues](https://github.com/yourusername/nochatbot/issues) page
2. Look for issues labeled `good first issue` or `help wanted`
3. Comment on the issue to express your interest
4. Wait for maintainer approval before starting work

### Reporting Bugs

Before creating a bug report:

1. Check existing issues to avoid duplicates
2. Collect relevant information (OS, Python version, error messages)
3. Create a minimal reproducible example

Bug report template:

```markdown
**Description**
A clear description of the bug.

**To Reproduce**
Steps to reproduce the behavior:
1. Run command '...'
2. See error

**Expected Behavior**
What you expected to happen.

**Environment**
- OS: [e.g., Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- No Chat Bot version: [e.g., 0.1.0]

**Additional Context**
Any other relevant information.
```

### Suggesting Features

Feature request template:

```markdown
**Problem Statement**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Other approaches you've considered.

**Additional Context**
Any other relevant information.
```

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/nochatbot.git
cd nochatbot

# Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/nochatbot.git
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install package in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 4. Set Up Environment Variables

```bash
# Create .env file
cp .env.example .env

# Add your API keys
echo "ANTHROPIC_API_KEY=your-key-here" >> .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### 5. Verify Installation

```bash
# Run tests to verify setup
pytest

# Check code formatting
black --check nochatbot/

# Run type checking
mypy nochatbot/
```

## Code Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- Line length: 100 characters (not 79)
- Use double quotes for strings
- Use type hints for all function signatures

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all code
black nochatbot/

# Check formatting without changes
black --check nochatbot/
```

### Type Checking

We use [mypy](http://mypy-lang.org/) for static type checking:

```bash
# Run type checking
mypy nochatbot/
```

All new code should include type hints:

```python
def process_data(input: str, max_length: int = 100) -> Dict[str, Any]:
    """Process input data and return results.
    
    Args:
        input: Input string to process
        max_length: Maximum length of output
        
    Returns:
        Dictionary containing processed results
    """
    pass
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 nochatbot/
```

### Documentation

- All public functions, classes, and modules must have docstrings
- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functionality

Example:

```python
def generate_questions(context: Dict[str, Any]) -> QuestionResult:
    """Generate intelligent questions based on context.
    
    This function analyzes the provided context and generates 8 high-quality
    options for users to choose from.
    
    Args:
        context: Dictionary containing:
            - type: Context type ('first_time', 'subsequent', 'from_chat')
            - scan_results: Project scan results (optional)
            - selection_history: Previous selections (optional)
            
    Returns:
        QuestionResult containing question and 8 options
        
    Raises:
        ValueError: If context is invalid
        
    Example:
        >>> context = {'type': 'first_time', 'scan_results': {...}}
        >>> result = generate_questions(context)
        >>> print(result.question)
        "What aspect of the project would you like to explore?"
    """
    pass
```

## Testing Guidelines

### Writing Tests

- Write tests for all new functionality
- Maintain or improve code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

Example:

```python
import pytest
from nochatbot.config import Config

def test_config_creates_default_file():
    """Test that Config creates default configuration file."""
    # Arrange
    config = Config()
    
    # Act
    config.ensure_config_exists()
    
    # Assert
    assert config.CONFIG_FILE.exists()
    assert config.config['version'] == '1.0.0'

def test_add_provider_validates_input():
    """Test that add_provider validates input parameters."""
    # Arrange
    config = Config()
    
    # Act & Assert
    with pytest.raises(ValueError, match="Provider name cannot be empty"):
        config.add_provider("", "api-key")
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_config.py

# Run specific test
pytest tests/test_config.py::test_config_creates_default_file

# Run with coverage
pytest --cov=nochatbot --cov-report=html

# Run with verbose output
pytest -v
```

### Test Coverage

- Aim for at least 80% code coverage
- Focus on testing critical paths and edge cases
- Don't sacrifice test quality for coverage numbers

```bash
# Generate coverage report
pytest --cov=nochatbot --cov-report=html

# View report
open htmlcov/index.html
```

## Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(scanner): add support for TypeScript files

Implement TypeScript file parsing in the scanner engine.
Includes support for .ts and .tsx files.

Closes #123
```

```
fix(config): handle missing config file gracefully

Previously, the application would crash if config file was missing.
Now it creates a default config file automatically.

Fixes #456
```

```
docs(readme): update installation instructions

Add instructions for Windows users and clarify Python version requirements.
```

### Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Keep subject line under 50 characters
- Capitalize subject line
- Don't end subject line with period
- Separate subject from body with blank line
- Wrap body at 72 characters
- Use body to explain what and why, not how

## Pull Request Process

### Before Submitting

1. **Update your fork**:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write code following our standards
   - Add tests for new functionality
   - Update documentation as needed

4. **Run quality checks**:
   ```bash
   # Format code
   black nochatbot/
   
   # Run linter
   flake8 nochatbot/
   
   # Type checking
   mypy nochatbot/
   
   # Run tests
   pytest
   ```

5. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat(component): add new feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

### Submitting Pull Request

1. Go to the original repository on GitHub
2. Click "New Pull Request"
3. Select your fork and branch
4. Fill out the PR template:

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings generated
```

### Review Process

1. Maintainers will review your PR
2. Address any requested changes
3. Push updates to your branch (PR updates automatically)
4. Once approved, maintainers will merge your PR

### After Merge

1. Delete your feature branch:
   ```bash
   git branch -d feature/your-feature-name
   git push origin --delete feature/your-feature-name
   ```

2. Update your local main:
   ```bash
   git checkout main
   git pull upstream main
   ```

## Project Structure

```
nochatbot/
├── nochatbot/              # Main package
│   ├── __init__.py
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Configuration management
│   ├── providers/         # AI provider implementations
│   │   ├── base.py        # Base provider interface
│   │   ├── claude.py      # Anthropic Claude provider
│   │   ├── openai.py      # OpenAI provider
│   │   └── deepseek.py    # DeepSeek provider
│   ├── scanner/           # Code scanning engine
│   │   ├── file_discovery.py
│   │   ├── master_agent.py
│   │   ├── sub_agent.py
│   │   └── task_queue.py
│   ├── recommendation/    # Question generation
│   │   └── question_generator.py
│   └── interaction/       # Chat bot and context
│       ├── chatbot.py
│       └── context.py
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Example scripts
├── pyproject.toml         # Project configuration
├── setup.py              # Setup script
├── requirements.txt       # Dependencies
├── README.md             # Main documentation
├── LICENSE               # MIT License
└── CONTRIBUTING.md       # This file
```

## Questions?

If you have questions:

1. Check existing documentation
2. Search closed issues
3. Ask in discussions
4. Open a new issue with the `question` label

Thank you for contributing to No Chat Bot!

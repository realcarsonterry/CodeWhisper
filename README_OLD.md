<div align="center">

# 🔮 CodeWhisper

### *Zero-Barrier AI Assistant for Intelligent Codebase Understanding*

[![Version](https://img.shields.io/badge/version-0.2.0-blue.svg)](https://github.com/realcarsonterry/codewhisper)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![AI Providers](https://img.shields.io/badge/AI%20providers-11+-purple.svg)]()

[Features](#-key-features) • [Quick Start](#-quick-start) • [AI Providers](#-supported-ai-providers) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Why CodeWhisper?

Traditional code analysis tools require you to know what to ask. **CodeWhisper flips the script.**

Instead of writing prompts, CodeWhisper:
- 🤖 **Proactively understands** your codebase through parallel AI agents
- 💡 **Asks intelligent questions** to guide your exploration
- 🕸️ **Builds a knowledge graph** connecting code relationships
- 🎯 **Provides contextual assistance** based on your journey through the code
- 🌐 **Works with ANY AI provider** - use your preferred model or mix multiple providers

Perfect for:
- 🚀 Onboarding to unfamiliar codebases
- 🔍 Understanding complex system architectures
- 📚 Documenting legacy projects
- 🐛 Debugging across multiple files
- 🎓 Learning from real-world code
- 🔄 Migrating between technologies

---

## ✨ Key Features

### 🤖 Universal AI Provider Support

Work with **11+ AI providers** out of the box. Mix and match for optimal results:

| Provider | Models | Best For |
|----------|--------|----------|
| **Anthropic Claude** | Opus, Sonnet, Haiku | Deep code understanding, complex reasoning |
| **OpenAI** | GPT-4, GPT-4 Turbo, GPT-3.5 | General purpose, fast responses |
| **Google Gemini** | Gemini Pro, 1.5 Pro, 1.5 Flash | Multimodal analysis, large context |
| **DeepSeek** | DeepSeek-Chat, DeepSeek-Coder | Code-specific tasks, cost-effective |
| **GLM (智谱AI)** | GLM-4-Plus, GLM-4 | Chinese codebases, bilingual support |
| **Qwen (通义千问)** | Qwen-Max, Qwen-Plus, Qwen-Turbo | Alibaba Cloud, Chinese language |
| **Moonshot (月之暗面)** | Moonshot-v1-8k/32k/128k | Long context, Chinese support |
| **Mistral AI** | Mistral Large, Medium, Small | European alternative, privacy-focused |
| **Cohere** | Command, Command-R, Command-R+ | Enterprise features, RAG optimization |
| **Baidu ERNIE** | ERNIE-4.0, ERNIE-3.5 | Chinese market, Baidu ecosystem |
| **Hugging Face** | Any HF model | Open source models, self-hosted |

### ⚡ Parallel Scanning Architecture
- **Master-Agent Coordination**: Intelligent task distribution
- **Configurable Agent Count**: Scale from 1 to 100+ parallel agents
- **Async/Await Optimization**: Efficient API call management
- **Thread-Based Parallelization**: Maximum throughput

### 🧠 Zero-Prompt Interaction
- **Progressive Questioning**: 8 high-quality options at each step
- **Context-Aware Recommendations**: Based on your selection history
- **Seamless Mode Switching**: Guided exploration ↔ Free chat
- **Intelligent Follow-ups**: AI anticipates your needs

### 📊 Knowledge Graph Construction
- **Automatic Relationship Mapping**: Files, functions, dependencies
- **Semantic Understanding**: Beyond syntax to intent
- **Visual Exploration**: Navigate code relationships
- **Incremental Updates**: Efficient re-scanning

### 🔒 Privacy-First Design
- **Explicit Permissions**: User-controlled access
- **Configurable Exclusions**: Protect sensitive data
- **Local Knowledge Base**: Your data stays on your machine
- **Transparent Processing**: Clear data usage policies

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codewhisper.git
cd codewhisper

# Install with pip
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Initial Configuration

```bash
# Initialize configuration
codewhisper init

# Add your first AI provider
codewhisper add-provider -n anthropic -k YOUR_API_KEY -m claude-opus-4-20250514

# Check status
codewhisper status
```

### Your First Scan

```bash
# Scan a project directory
codewhisper scan /path/to/your/project

# Scan with specific provider and agent count
codewhisper scan . --provider anthropic --max-agents 20

# Non-interactive scan (results only)
codewhisper scan ~/code/myapp --no-interactive
```

---

## 📖 Documentation

### Table of Contents
- [Installation Guide](#-installation-guide)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Architecture Overview](#-architecture)
- [API Provider Setup](#-api-provider-setup)
- [Advanced Features](#-advanced-features)
- [Performance Benchmarks](#-performance-benchmarks)
- [Troubleshooting](#-troubleshooting)

---

## 🔧 Installation Guide

### System Requirements

- **Python**: 3.8 or higher
- **Operating System**: Windows, macOS, Linux
- **Memory**: 2GB RAM minimum (4GB+ recommended for large projects)
- **Storage**: 100MB for application + space for knowledge base
- **Network**: Internet connection for AI API calls

### Installation Methods

#### Method 1: Install from Source (Recommended)

```bash
# Clone repository
git clone https://github.com/yourusername/codewhisper.git
cd codewhisper

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install package
pip install -e .
```

#### Method 2: Install from PyPI (Coming Soon)

```bash
pip install codewhisper
```

#### Method 3: Development Installation

```bash
# Install with all development dependencies
pip install -e ".[dev]"

# Verify installation
pytest
black --check nochatbot/
mypy nochatbot/
```

### Verifying Installation

```bash
# Check version
codewhisper --version

# View help
codewhisper --help

# Initialize configuration
codewhisper init
```

---

## ⚙️ Configuration

### Configuration File Location

CodeWhisper stores configuration at `~/.codewhisper/config.json`

### Configuration Structure

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-...",
      "model": "claude-opus-4-20250514"
    },
    "openai": {
      "api_key": "sk-...",
      "model": "gpt-4"
    },
    "deepseek": {
      "api_key": "sk-...",
      "model": "deepseek-chat"
    },
    "glm": {
      "api_key": "xxx.yyy",
      "model": "glm-4-plus"
    }
  },
  "scanning": {
    "max_agents": 100,
    "exclude_dirs": [
      "node_modules",
      ".git",
      "__pycache__",
      ".venv",
      "venv",
      "dist",
      "build"
    ],
    "exclude_files": [
      "*.pyc",
      "*.log",
      ".DS_Store"
    ],
    "max_file_size_mb": 10
  },
  "knowledge_base": {
    "path": "~/.codewhisper/knowledge",
    "vector_db": "chromadb"
  },
  "privacy": {
    "permissions_granted": false,
    "exclude_paths": []
  }
}
```

### Managing Configuration

```bash
# View current configuration
codewhisper status

# Add a provider
codewhisper add-provider -n anthropic -k YOUR_KEY -m claude-opus-4-20250514

# List all providers
nochatbot list-providers

# Reset configuration
codewhisper init
```

---

## 💡 Usage Examples

### Command Line Interface

#### Basic Scanning

```bash
# Scan current directory
codewhisper scan .

# Scan specific path
codewhisper scan /path/to/project

# Scan with custom agent count
codewhisper scan . --max-agents 50
```

#### Provider Selection

```bash
# Use specific provider
codewhisper scan . --provider openai

# Use all configured providers (default)
codewhisper scan .
```

#### Interactive Mode

After scanning, CodeWhisper launches an interactive interface:

```
Chat with your codebase! Ask questions about the scanned project.

You: What is the main entry point of this application?
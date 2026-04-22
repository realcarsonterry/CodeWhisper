### ⚡ Parallel Scanning Architecture

```
Master Agent
    ├── Sub-Agent 1 (Claude Opus)    → Analyzing auth.py
    ├── Sub-Agent 2 (GPT-4)          → Analyzing database.py
    ├── Sub-Agent 3 (Gemini Pro)     → Analyzing api.py
    ├── Sub-Agent 4 (DeepSeek)       → Analyzing utils.py
    └── Sub-Agent N (...)            → Analyzing ...
         ↓
    Knowledge Graph Builder
         ↓
    Intelligent Recommendations
```

- **Master-Agent Coordination**: Intelligent task distribution
- **Configurable Agent Count**: Scale from 1 to 100+ parallel agents
- **Async/Await Optimization**: Efficient API call management
- **Provider Load Balancing**: Distribute work across multiple AI providers
- **Cost Optimization**: Use cheaper models for simple files, premium models for complex code

### 🧠 Zero-Prompt Interaction

- **Progressive Questioning**: 8 high-quality options at each step
- **Context-Aware Recommendations**: Based on your selection history
- **Seamless Mode Switching**: Guided exploration ↔ Free chat
- **Intelligent Follow-ups**: AI anticipates your needs
- **Multi-Language Support**: Works with any programming language

### 📊 Knowledge Graph Construction

- **Automatic Relationship Mapping**: Files, functions, dependencies
- **Semantic Understanding**: Beyond syntax to intent
- **Visual Exploration**: Navigate code relationships
- **Incremental Updates**: Efficient re-scanning
- **Cross-File Analysis**: Understand how components interact

### 🔒 Privacy-First Design

- **Explicit Permissions**: User-controlled access
- **Configurable Exclusions**: Protect sensitive data
- **Local Knowledge Base**: Your data stays on your machine
- **Transparent Processing**: Clear data usage policies
- **Provider Choice**: Use self-hosted models if needed

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/realcarsonterry/codewhisper.git
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

# Add your first AI provider (choose one or add multiple)
codewhisper add-provider -n anthropic -k YOUR_API_KEY -m claude-opus-4-20250514
codewhisper add-provider -n openai -k YOUR_API_KEY -m gpt-4
codewhisper add-provider -n gemini -k YOUR_API_KEY -m gemini-1.5-pro

# Check status
codewhisper status
```

### Your First Scan

```bash
# Scan a project directory
codewhisper scan /path/to/your/project

# Scan with specific provider and agent count
codewhisper scan . --provider anthropic --max-agents 20

# Use multiple providers for load balancing
codewhisper scan ~/code/myapp --max-agents 50

# Non-interactive scan (results only)
codewhisper scan . --no-interactive
```

---

## 🌐 Supported AI Providers

### 1. Anthropic Claude

**Best for**: Deep code understanding, complex reasoning, long context

```bash
# Add provider
codewhisper add-provider -n anthropic -k sk-ant-xxx -m claude-opus-4-20250514

# Available models
claude-opus-4-20250514    # Most capable, best for complex analysis
claude-sonnet-4-20250514  # Balanced performance and cost
claude-haiku-3-20240307   # Fast and cost-effective
```

**Get API Key**: https://console.anthropic.com/

---

### 2. OpenAI

**Best for**: General purpose, fast responses, wide adoption

```bash
# Add provider
codewhisper add-provider -n openai -k sk-xxx -m gpt-4-turbo

# Available models
gpt-4-turbo              # Latest GPT-4 with 128k context
gpt-4                    # Standard GPT-4
gpt-3.5-turbo           # Fast and economical
```

**Get API Key**: https://platform.openai.com/api-keys

---

### 3. Google Gemini

**Best for**: Multimodal analysis, large context windows, free tier

```bash
# Add provider
codewhisper add-provider -n gemini -k YOUR_API_KEY -m gemini-1.5-pro

# Available models
gemini-1.5-pro          # 1M token context, best quality
gemini-1.5-flash        # Fast and efficient
gemini-pro              # Standard model
```

**Get API Key**: https://makersuite.google.com/app/apikey

---

### 4. DeepSeek

**Best for**: Code-specific tasks, cost-effective, Chinese support

```bash
# Add provider
codewhisper add-provider -n deepseek -k sk-xxx -m deepseek-chat

# Available models
deepseek-chat           # General chat model
deepseek-coder          # Specialized for code
```

**Get API Key**: https://platform.deepseek.com/

---

### 5. GLM (智谱AI / Zhipu AI)

**Best for**: Chinese codebases, bilingual support, domestic deployment

```bash
# Add provider
codewhisper add-provider -n glm -k xxx.yyy -m glm-4-plus

# Available models
glm-4-plus              # Most capable
glm-4                   # Standard model
glm-3-turbo             # Fast and economical
```

**Get API Key**: https://open.bigmodel.cn/

---

### 6. Qwen (通义千问 / Alibaba Cloud)

**Best for**: Alibaba Cloud ecosystem, Chinese language, enterprise

```bash
# Add provider
codewhisper add-provider -n qwen -k sk-xxx -m qwen-max

# Available models
qwen-max                # Most capable
qwen-plus               # Balanced
qwen-turbo              # Fast and economical
```

**Get API Key**: https://dashscope.console.aliyun.com/

---

### 7. Moonshot (月之暗面 / Kimi)

**Best for**: Long context (up to 128k), Chinese support, memory

```bash
# Add provider
codewhisper add-provider -n moonshot -k sk-xxx -m moonshot-v1-32k

# Available models
moonshot-v1-128k        # 128k context window
moonshot-v1-32k         # 32k context window
moonshot-v1-8k          # 8k context window
```

**Get API Key**: https://platform.moonshot.cn/

---

### 8. Mistral AI

**Best for**: European alternative, privacy-focused, open models

```bash
# Add provider
codewhisper add-provider -n mistral -k xxx -m mistral-large-latest

# Available models
mistral-large-latest    # Most capable
mistral-medium-latest   # Balanced
mistral-small-latest    # Fast and economical
```

**Get API Key**: https://console.mistral.ai/

---

### 9. Cohere

**Best for**: Enterprise features, RAG optimization, embeddings

```bash
# Add provider
codewhisper add-provider -n cohere -k xxx -m command-r-plus

# Available models
command-r-plus          # Most capable, RAG optimized
command-r               # Balanced
command                 # Standard model
```

**Get API Key**: https://dashboard.cohere.com/

---

### 10. Baidu ERNIE (文心一言)

**Best for**: Chinese market, Baidu ecosystem, domestic deployment

```bash
# Add provider
codewhisper add-provider -n ernie -k xxx -m ernie-4.0

# Available models
ernie-4.0               # Most capable
ernie-3.5               # Balanced
ernie-turbo             # Fast and economical
```

**Get API Key**: https://console.bce.baidu.com/qianfan/

---

### 11. Hugging Face

**Best for**: Open source models, self-hosted, customization

```bash
# Add provider
codewhisper add-provider -n huggingface -k hf_xxx -m meta-llama/Llama-2-70b-chat-hf

# Use any model from Hugging Face Hub
# Examples:
meta-llama/Llama-2-70b-chat-hf
mistralai/Mixtral-8x7B-Instruct-v0.1
codellama/CodeLlama-34b-Instruct-hf
```

**Get API Key**: https://huggingface.co/settings/tokens

---

## 📖 Advanced Usage

### Multi-Provider Strategy

Use different providers for different tasks:

```bash
# Use Claude for complex analysis
codewhisper scan ./backend --provider anthropic --max-agents 10

# Use GPT-4 for frontend code
codewhisper scan ./frontend --provider openai --max-agents 20

# Use DeepSeek for cost-effective bulk scanning
codewhisper scan ./tests --provider deepseek --max-agents 50
```

### Load Balancing

When you configure multiple providers, CodeWhisper automatically distributes work:

```bash
# Configure multiple providers
codewhisper add-provider -n anthropic -k xxx -m claude-opus-4-20250514
codewhisper add-provider -n openai -k xxx -m gpt-4-turbo
codewhisper add-provider -n gemini -k xxx -m gemini-1.5-pro

# Scan with load balancing (round-robin across all providers)
codewhisper scan ./large-project --max-agents 60
# Agent 1: Claude, Agent 2: OpenAI, Agent 3: Gemini, Agent 4: Claude, ...
```

### Cost Optimization

```bash
# Use cheaper models for initial scan
codewhisper add-provider -n openai -k xxx -m gpt-3.5-turbo
codewhisper scan . --provider openai --max-agents 50

# Then use premium models for specific questions
codewhisper add-provider -n anthropic -k xxx -m claude-opus-4-20250514
# Interactive mode will use Claude for detailed analysis
```

---

## 💰 Cost Comparison

Approximate costs per 1M tokens (as of 2025):

| Provider | Input | Output | Notes |
|----------|-------|--------|-------|
| Claude Opus | $15 | $75 | Best quality |
| Claude Sonnet | $3 | $15 | Balanced |
| GPT-4 Turbo | $10 | $30 | Fast |
| GPT-3.5 Turbo | $0.50 | $1.50 | Economical |
| Gemini Pro | Free* | Free* | Generous free tier |
| DeepSeek | $0.14 | $0.28 | Very cheap |
| GLM-4-Plus | ¥0.05 | ¥0.05 | ~$0.007 |
| Qwen-Max | ¥0.04 | ¥0.12 | ~$0.006-$0.017 |
| Moonshot | ¥0.012 | ¥0.012 | ~$0.0017 |

*Gemini has generous free tier limits

**Cost Optimization Tips:**
- Use cheaper models (GPT-3.5, DeepSeek, GLM) for initial scanning
- Use premium models (Claude Opus, GPT-4) for complex analysis
- Mix providers to balance cost and quality
- Chinese providers (GLM, Qwen, Moonshot) are extremely cost-effective

---

## 🎯 Use Cases

### 1. Onboarding to New Codebase

```bash
# Scan the entire project
codewhisper scan ~/new-project --max-agents 30

# CodeWhisper will ask:
# 1. "Would you like to understand the overall architecture?"
# 2. "Which module interests you most?"
# 3. "Should I explain the authentication flow?"
# ... and 5 more intelligent questions
```

### 2. Debugging Complex Issues

```bash
# Scan specific modules
codewhisper scan ./src/payment --provider anthropic

# Ask targeted questions in interactive mode
# CodeWhisper understands the context and relationships
```

### 3. Code Review Preparation

```bash
# Scan changed files
codewhisper scan ./src --max-agents 20

# Get insights about:
# - Code quality issues
# - Potential bugs
# - Architecture concerns
# - Best practice violations
```

---

## 🔧 CLI Commands

```bash
# Initialize configuration
codewhisper init

# Add/update AI provider
codewhisper add-provider -n <name> -k <api-key> -m <model>

# List all configured providers
codewhisper list-providers

# Show configuration status
codewhisper status

# Scan a directory
codewhisper scan <path> [OPTIONS]
  --provider TEXT        Specific provider to use
  --max-agents INTEGER   Maximum parallel agents (default: 10)
  --no-interactive       Skip interactive mode

# Show version
codewhisper --version

# Show help
codewhisper --help
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Adding New AI Providers

To add a new AI provider:

1. Create a new file in `codewhisper/providers/`
2. Extend the `AIProvider` base class
3. Implement required methods:
   - `async send_message()`
   - `async stream_response()`
   - `get_cost_per_token()`
4. Add to `codewhisper/providers/__init__.py`
5. Update CLI to support the new provider
6. Add documentation and tests

See existing providers for examples.

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---


---

## 📞 Support

- **Issues**: https://github.com/realcarsonterry/codewhisper/issues
- **Discussions**: https://github.com/realcarsonterry/codewhisper/discussions

---

<div align="center">

**Made with ❤️ by developers, for developers**

[⭐ Star us on GitHub](https://github.com/realcarsonterry/codewhisper) • [🐛 Report Bug](https://github.com/realcarsonterry/codewhisper/issues) • [💡 Request Feature](https://github.com/realcarsonterry/codewhisper/issues)

</div>

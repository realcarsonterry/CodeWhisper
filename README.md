# CodeWhisper

<div align="center">

### **Making No-Chatbot a Reality**

*An AI-powered code intelligence system that predicts what you want to know, instead of making you ask*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Development Status](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/realcarsonterry/CodeWhisper)

[Features](#-core-architecture) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 🎯 Vision

Traditional AI assistants require you to articulate your questions clearly. But what if you don't know what to ask? What if you're exploring unfamiliar code and need guidance on where to start?

**CodeWhisper inverts this paradigm.**

Instead of waiting for your questions, CodeWhisper deploys hundreds of autonomous AI agents to deeply understand your codebase, then **proactively predicts** what you want to know. You simply choose from 8 intelligently-generated options, and the system progressively refines its understanding until it surfaces exactly what you need.

This is **No-Chatbot**: AI that anticipates your needs, not one that waits for instructions.

---

## 🧠 Core Architecture

### Multi-Agent Orchestration

```
┌─────────────────────────────────────────────────────────────┐
│                      Master Agent                            │
│  • Task Distribution    • Health Monitoring                  │
│  • Load Balancing      • Failure Recovery                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
   ┌────▼────┐          ┌────▼────┐
   │ Sub-Agent Pool     │ Sub-Agent Pool     │
   │ ├─ Agent 1         │ ├─ Agent N         │
   │ ├─ Agent 2         │ ├─ Agent N+1       │
   │ └─ Agent ...       │ └─ Agent ...       │
   └────┬────┘          └────┬────┘
        │                     │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Knowledge Graph     │
        │  • Semantic Nodes    │
        │  • Relationship Edges│
        │  • Context Vectors   │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Prediction Engine   │
        │  • Need Inference    │
        │  • Option Generation │
        │  • Progressive Refinement │
        └─────────────────────┘
```

### Operational Flow

**Phase 1: Distributed Scanning**
- Master agent spawns hundreds/thousands of sub-agents (one per file)
- Each sub-agent independently analyzes its assigned file
- Parallel execution with automatic API failover and load balancing
- Results aggregated into a unified knowledge graph

**Phase 2: Continuous Background Reasoning**
- Sub-agents continuously communicate and exchange insights
- Collaborative inference about user intent based on codebase characteristics
- Dynamic prediction model updates based on user interaction patterns

**Phase 3: Progressive Interaction**
- **No-Chat Mode** (Default): System presents 8 predicted options + 1 mode switch
- User selects an option → Sub-agents refine predictions → New 8+1 options
- Iterative refinement from broad categories to granular specifics
- **Chat Mode** (Optional): Traditional Q&A with full codebase context
- Seamless mode switching preserves conversation context

---

## ✨ Key Features

### 🎯 Predictive Intelligence
- **Zero-Prompt Interaction**: No need to formulate questions
- **Progressive Refinement**: From high-level concepts to implementation details
- **Context Accumulation**: Each interaction deepens system understanding
- **Adaptive Learning**: Prediction model evolves with your workflow

### ⚡ Massive Parallelism
- **True Concurrency**: One agent per file, hundreds running simultaneously
- **Async Architecture**: Non-blocking I/O for maximum throughput
- **Smart Throttling**: Respects API rate limits while maximizing speed
- **Fault Tolerance**: Automatic failover across multiple AI providers

### 🌐 Multi-Provider Ecosystem
- **11+ AI Providers**: Claude, GPT-4, Gemini, DeepSeek, GLM, Qwen, Moonshot, and more
- **Automatic Health Checks**: Pre-scan validation of all configured APIs
- **Intelligent Failover**: Seamless switching when providers fail
- **Cost Optimization**: Mix premium and economical models strategically

### 🔄 Dual-Mode Interface
- **No-Chat Mode**: AI-driven guided exploration
- **Chat Mode**: Traditional conversational interface
- **Seamless Switching**: Preserve context across mode transitions
- **Unified Knowledge Base**: Both modes leverage the same deep understanding

---

## 🚀 Quick Start

### Installation

```bash
git clone https://github.com/realcarsonterry/CodeWhisper.git
cd CodeWhisper
pip install -e .
```

### Configuration

```bash
# Add AI providers (recommend multiple for redundancy)
codewhisper add-provider -n anthropic -k YOUR_API_KEY -m claude-opus-4-20250514
codewhisper add-provider -n openai -k YOUR_API_KEY -m gpt-4-turbo
codewhisper add-provider -n deepseek -k YOUR_API_KEY -m deepseek-coder

# Verify configuration
codewhisper status
```

### Usage

```bash
# Navigate to your project
cd /path/to/your/codebase

# Launch CodeWhisper
codewhisper scan .

# System will:
# 1. Validate API health across all providers
# 2. Deploy sub-agents for parallel file analysis
# 3. Construct knowledge graph
# 4. Enter No-Chat mode with 8 predicted options
```

### Example Session

```
╔══════════════════════════════════════════════════════════════╗
║  Welcome to CodeWhisper - Intelligent Code Assistant         ║
╚══════════════════════════════════════════════════════════════╝

Session ID: b62d667f-6b76-4d4a-9bcb-6a23c97b4029
Project: my-web-app

Scan Results:
  Files scanned:     247
  Files analyzed:    247
  Knowledge nodes:   1,893
  Knowledge edges:   5,421

══════════════════════════════════════════════════════════════
No Chat Mode
══════════════════════════════════════════════════════════════

Based on comprehensive analysis of your codebase, you likely want to:

[1] Understand the overall system architecture
    Explore high-level design patterns, module boundaries, and data flow

[2] Investigate authentication and authorization mechanisms
    Deep dive into security implementation, session management, and access control

[3] Analyze database schema and ORM relationships
    Examine data models, migrations, and query patterns

[4] Review API endpoint design and routing logic
    Understand RESTful structure, middleware chain, and request handling

[5] Identify performance bottlenecks and optimization opportunities
    Analyze computational complexity, database queries, and caching strategies

[6] Examine test coverage and quality assurance practices
    Review unit tests, integration tests, and CI/CD configuration

[7] Explore deployment architecture and infrastructure code
    Investigate containerization, orchestration, and environment configuration

[8] Assess code quality, maintainability, and technical debt
    Evaluate adherence to best practices, design patterns, and refactoring needs

[9] Switch to Chat Mode
    Have a free conversation with the AI assistant

──────────────────────────────────────────────────────────────
Your choice (1-9): _
```

---

## 🛠️ Supported AI Providers

| Provider | Model | Strengths | API Key |
|----------|-------|-----------|---------|
| **Anthropic Claude** | claude-opus-4-20250514 | Superior reasoning, long context | [Get Key](https://console.anthropic.com/) |
| **OpenAI** | gpt-4-turbo | Fast, versatile, widely adopted | [Get Key](https://platform.openai.com/api-keys) |
| **Google Gemini** | gemini-1.5-pro | 1M token context, multimodal | [Get Key](https://makersuite.google.com/app/apikey) |
| **DeepSeek** | deepseek-coder | Code-specialized, cost-effective | [Get Key](https://platform.deepseek.com/) |
| **GLM (Zhipu AI)** | glm-4-plus | Chinese language, bilingual | [Get Key](https://open.bigmodel.cn/) |
| **Qwen (Alibaba)** | qwen-max | Enterprise-grade, Alibaba ecosystem | [Get Key](https://dashscope.console.aliyun.com/) |
| **Moonshot (Kimi)** | moonshot-v1-128k | Ultra-long context (128k tokens) | [Get Key](https://platform.moonshot.cn/) |
| **Mistral AI** | mistral-large-latest | European, privacy-focused | [Get Key](https://console.mistral.ai/) |
| **Cohere** | command-r-plus | RAG-optimized, enterprise features | [Get Key](https://dashboard.cohere.com/) |
| **Baidu ERNIE** | ernie-4.0 | Chinese market, Baidu integration | [Get Key](https://console.bce.baidu.com/qianfan/) |
| **HuggingFace** | Any OSS model | Self-hosted, customizable | [Get Key](https://huggingface.co/settings/tokens) |

### Cost Optimization Strategy

```bash
# Tier 1: Initial scanning (use economical models)
codewhisper add-provider -n deepseek -k KEY -m deepseek-coder  # ~$0.14/1M tokens
codewhisper add-provider -n glm -k KEY -m glm-4-plus           # ~$0.007/1M tokens

# Tier 2: Deep analysis (use premium models)
codewhisper add-provider -n anthropic -k KEY -m claude-opus-4  # $15/1M tokens
codewhisper add-provider -n openai -k KEY -m gpt-4-turbo       # $10/1M tokens

# System automatically uses Tier 1 for scanning, Tier 2 for complex reasoning
```

---

## 📖 Documentation

### CLI Reference

```bash
# Initialize configuration
codewhisper init

# Provider management
codewhisper add-provider -n <provider> -k <api-key> -m <model>
codewhisper list-providers
codewhisper status

# Scanning
codewhisper scan <path> [OPTIONS]
  --provider TEXT        Use specific provider
  --max-agents INTEGER   Parallel agent count (default: 1000)
  --no-interactive       Skip interactive mode

# Help
codewhisper --help
codewhisper scan --help
```

### Advanced Usage

**Multi-Provider Load Balancing**
```bash
# Configure multiple providers
codewhisper add-provider -n anthropic -k KEY1 -m claude-opus-4
codewhisper add-provider -n openai -k KEY2 -m gpt-4-turbo
codewhisper add-provider -n gemini -k KEY3 -m gemini-1.5-pro

# Scan with automatic round-robin distribution
codewhisper scan ./large-project --max-agents 300
# Agent 1→Claude, Agent 2→OpenAI, Agent 3→Gemini, Agent 4→Claude, ...
```

**Selective Scanning**
```bash
# Scan specific modules
codewhisper scan ./backend/auth --provider anthropic --max-agents 20
codewhisper scan ./frontend/components --provider openai --max-agents 50

# Non-interactive mode for CI/CD
codewhisper scan . --no-interactive > scan-report.txt
```

---

## ⚠️ Project Status

**CodeWhisper is currently in alpha stage.**

### What Works
- ✅ Distributed parallel scanning with hundreds of agents
- ✅ Multi-provider support with automatic failover
- ✅ Knowledge graph construction
- ✅ No-Chat mode with 8+1 option generation
- ✅ Chat mode with full codebase context
- ✅ Seamless mode switching

### Known Limitations
- ⚠️ Background sub-agent reasoning not fully implemented
- ⚠️ Prediction quality varies with codebase complexity
- ⚠️ Large codebases (10,000+ files) may experience performance issues
- ⚠️ Knowledge graph visualization not yet available
- ⚠️ Limited test coverage

### Roadmap
- [ ] Implement persistent background reasoning engine
- [ ] Enhance prediction model with reinforcement learning
- [ ] Add knowledge graph visualization interface
- [ ] Optimize performance for massive codebases
- [ ] Expand test coverage to 80%+
- [ ] Add support for more AI providers
- [ ] Develop plugin system for extensibility

---

## 🤝 Contributing

**This project needs your help.**

CodeWhisper is an ambitious attempt to fundamentally change how developers interact with AI. While the core architecture is in place, there's significant work ahead to realize the full vision.

### How to Contribute

**Report Issues**
- Found a bug? [Open an issue](https://github.com/realcarsonterry/CodeWhisper/issues)
- Have a feature idea? [Start a discussion](https://github.com/realcarsonterry/CodeWhisper/discussions)

**Submit Code**
- Fork the repository
- Create a feature branch (`git checkout -b feature/amazing-feature`)
- Commit your changes (`git commit -m 'Add amazing feature'`)
- Push to the branch (`git push origin feature/amazing-feature`)
- Open a Pull Request

**Areas Needing Help**
- 🧠 Prediction model optimization
- ⚡ Performance tuning for large codebases
- 🎨 Knowledge graph visualization
- 📝 Documentation and tutorials
- 🧪 Test coverage expansion
- 🌐 Additional AI provider integrations

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---



## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 📞 Contact

- **Issues**: https://github.com/realcarsonterry/CodeWhisper/issues
- **Discussions**: https://github.com/realcarsonterry/CodeWhisper/discussions
- **Pull Requests**: https://github.com/realcarsonterry/CodeWhisper/pulls

---

<div align="center">

### **Let AI predict your needs, not wait for your questions**

*Making No-Chatbot a reality, one codebase at a time*

[⭐ Star this project](https://github.com/realcarsonterry/CodeWhisper) • [🐛 Report Bug](https://github.com/realcarsonterry/CodeWhisper/issues) • [💡 Request Feature](https://github.com/realcarsonterry/CodeWhisper/discussions)

</div>

# CodeWhisper

<div align="center">

**Make No-Chatbot Become Reality**

一个革命性的代码理解工具，让 AI 真正理解你的需求，而不是让你费力描述

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange.svg)](https://github.com/realcarsonterry/CodeWhisper)

[English](#english) | [中文](#中文)

</div>

---

## 中文

### 🎯 项目愿景

**CodeWhisper 的目标是让 "No-Chatbot" 成为现实。**

传统的 AI 聊天工具要求你清楚地描述问题，但很多时候你并不知道该问什么。CodeWhisper 反其道而行之：**让 AI 猜测你想做什么，而不是让你告诉 AI 该做什么。**

### 💡 核心理念

想象一下：
- 你打开一个陌生的代码仓库，不知道从哪里开始
- 你有个模糊的想法，但不知道如何用语言描述
- 你想改进代码，但不确定具体改什么

**CodeWhisper 会主动为你提供 8 个高质量的选项**，基于对整个代码库的深度理解，猜测你最可能想做的事情。你只需要选择一个数字，AI 就会继续深入，逐步细化，直到找到你真正想要的答案。

### 🚀 工作流程

```
1. 扫描阶段
   └─ Master Agent 部署成百上千个 Sub Agents
      └─ 并行扫描、读取、理解整个文件夹的所有文件
         └─ 构建完整的知识图谱

2. No-Chat 模式（默认）
   └─ 成百上千的 Sub Agents 在后台持续交流
      └─ 猜测用户需求
         └─ 生成 8 个高质量选项 + 1 个切换到 Chat 模式的选项
            └─ 用户选择一个选项
               └─ Sub Agents 根据选择重新思考
                  └─ 生成更细化的 8+1 选项
                     └─ 循环往复，逐步细化到极小颗粒度

3. Chat 模式（可选）
   └─ 用户自由输入问题
      └─ AI 基于完整代码库理解回答
         └─ 每次回答后提供切换回 No-Chat 模式的选项
            └─ 切换后，Sub Agents 根据对话内容重新生成 8+1 选项
```

### ✨ 核心特性

#### 🧠 智能问题预测
- **无需描述问题**：AI 主动猜测你想做什么
- **渐进式细化**：从大方向逐步细化到具体操作
- **上下文感知**：基于你的选择历史动态调整
- **双模式切换**：No-Chat ↔ Chat 无缝切换

#### ⚡ 大规模并行扫描
- **Master-Agent 架构**：一个 Master 协调成百上千个 Sub Agents
- **真正的并行**：每个文件一个 Agent，最大化扫描速度
- **多 AI 提供商**：支持 11+ AI 提供商，自动负载均衡
- **智能故障转移**：API 失败时自动切换到备用提供商

#### 🔄 持续后台思考
- **Sub Agents 协作**：扫描完成后持续在后台交流
- **需求预测**：基于代码库特征预测用户可能的需求
- **动态适应**：根据用户选择实时调整预测策略

#### 🌐 多 AI 提供商支持
支持 11+ AI 提供商，包括：
- **国际**：Claude (Anthropic), GPT (OpenAI), Gemini (Google), DeepSeek, Mistral, Cohere, HuggingFace
- **国内**：GLM (智谱), Qwen (通义千问), Moonshot (月之暗面), ERNIE (文心一言)

### 📦 快速开始

#### 安装

```bash
# 克隆仓库
git clone https://github.com/realcarsonterry/CodeWhisper.git
cd CodeWhisper

# 安装
pip install -e .
```

#### 配置 AI 提供商

```bash
# 添加一个或多个 AI 提供商（建议配置多个以实现自动故障转移）
codewhisper add-provider -n anthropic -k YOUR_API_KEY -m claude-opus-4-20250514
codewhisper add-provider -n openai -k YOUR_API_KEY -m gpt-4-turbo
codewhisper add-provider -n glm -k YOUR_API_KEY -m glm-4-plus
```

#### 开始使用

```bash
# 进入你想分析的项目目录
cd /path/to/your/project

# 启动扫描
codewhisper scan .

# 系统会：
# 1. 检查所有配置的 API 健康状态
# 2. 部署成百上千的 Sub Agents 并行扫描所有文件
# 3. 构建知识图谱
# 4. 进入 No-Chat 模式，提供 8+1 个智能选项
```

### 🎮 使用示例

```
欢迎使用 CodeWhisper！

扫描完成：
- 文件数：156
- 分析成功：156
- 知识节点：1,247
- 知识边：3,891

================== No Chat 模式 ==================

基于对整个代码库的理解，我猜测你可能想：

1. 了解项目的整体架构和模块划分
2. 查看认证和授权的实现方式
3. 理解数据库模型和关系
4. 分析 API 接口的设计
5. 查找潜在的性能瓶颈
6. 了解测试覆盖情况
7. 查看部署和配置相关代码
8. 分析代码质量和最佳实践

9. 切换到 Chat 模式（自由提问）

请选择 (1-9): _
```

### 🛠️ 支持的 AI 提供商

| 提供商 | 获取 API Key | 推荐模型 | 特点 |
|--------|-------------|---------|------|
| **Anthropic Claude** | [console.anthropic.com](https://console.anthropic.com/) | claude-opus-4-20250514 | 最强代码理解能力 |
| **OpenAI** | [platform.openai.com](https://platform.openai.com/api-keys) | gpt-4-turbo | 通用性强，响应快 |
| **Google Gemini** | [makersuite.google.com](https://makersuite.google.com/app/apikey) | gemini-1.5-pro | 超大上下文窗口 |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com/) | deepseek-coder | 代码专用，性价比高 |
| **GLM (智谱)** | [open.bigmodel.cn](https://open.bigmodel.cn/) | glm-4-plus | 中文支持好 |
| **Qwen (通义千问)** | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/) | qwen-max | 阿里云生态 |
| **Moonshot (月之暗面)** | [platform.moonshot.cn](https://platform.moonshot.cn/) | moonshot-v1-128k | 超长上下文 |
| **Mistral** | [console.mistral.ai](https://console.mistral.ai/) | mistral-large-latest | 欧洲隐私友好 |
| **Cohere** | [dashboard.cohere.com](https://dashboard.cohere.com/) | command-r-plus | 企业级 RAG |
| **ERNIE (文心)** | [console.bce.baidu.com/qianfan](https://console.bce.baidu.com/qianfan/) | ernie-4.0 | 百度生态 |
| **HuggingFace** | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | 任意开源模型 | 自托管，可定制 |

### 💰 成本优化建议

- **初始扫描**：使用便宜的模型（DeepSeek, GLM, Qwen）
- **深度分析**：使用高质量模型（Claude Opus, GPT-4）
- **混合策略**：配置多个提供商，自动负载均衡
- **国内提供商**：GLM、Qwen、Moonshot 性价比极高（约 $0.001-0.02/1M tokens）

### ⚠️ 项目状态

**本项目目前处于早期开发阶段（Alpha）**

- ✅ 核心功能已实现：并行扫描、知识图谱、No-Chat 模式
- ⚠️ 仍存在许多问题和待优化的地方
- 🚧 API 可能会发生变化
- 🐛 可能存在未发现的 Bug

**我们需要你的帮助！**

如果你对这个项目感兴趣，欢迎：
- 🐛 报告 Bug：[提交 Issue](https://github.com/realcarsonterry/CodeWhisper/issues)
- 💡 提出建议：[参与讨论](https://github.com/realcarsonterry/CodeWhisper/discussions)
- 🔧 贡献代码：[提交 Pull Request](https://github.com/realcarsonterry/CodeWhisper/pulls)
- ⭐ Star 本项目，让更多人看到

### 🎯 待解决的问题

- [ ] Sub Agents 后台持续思考机制尚未完全实现
- [ ] 问题生成的质量需要进一步优化
- [ ] 大型代码库（10,000+ 文件）的性能优化
- [ ] 知识图谱的可视化界面
- [ ] 更智能的上下文感知和需求预测
- [ ] 更多 AI 提供商的支持
- [ ] 完善的测试覆盖
- [ ] 详细的文档和教程

### 👨‍💻 关于作者

**本项目由 [Terry Carson YM](https://github.com/realcarsonterry) 独立开发。**

这不是 AI 生成的项目，而是一个真实的、由人类开发者创建的工具，旨在解决实际的代码理解问题。

虽然在开发过程中使用了 AI 辅助编码，但所有的架构设计、核心理念、功能规划都来自人类的思考和创造。

### 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

### 🤝 贡献指南

我们欢迎任何形式的贡献！无论是：
- 修复 Bug
- 添加新功能
- 改进文档
- 优化性能
- 提出建议

请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细的贡献指南。

### 📞 联系方式

- **GitHub Issues**: https://github.com/realcarsonterry/CodeWhisper/issues
- **GitHub Discussions**: https://github.com/realcarsonterry/CodeWhisper/discussions

---

<div align="center">

**让 AI 猜测你的需求，而不是让你描述问题**

[⭐ Star](https://github.com/realcarsonterry/CodeWhisper) • [🐛 报告问题](https://github.com/realcarsonterry/CodeWhisper/issues) • [💡 功能建议](https://github.com/realcarsonterry/CodeWhisper/discussions)

</div>

---

## English

### 🎯 Project Vision

**CodeWhisper aims to make "No-Chatbot" a reality.**

Traditional AI chat tools require you to clearly describe your problem, but often you don't know what to ask. CodeWhisper takes the opposite approach: **Let AI guess what you want to do, instead of making you tell AI what to do.**

### 💡 Core Concept

Imagine:
- You open an unfamiliar codebase and don't know where to start
- You have a vague idea but can't articulate it
- You want to improve code but aren't sure what specifically

**CodeWhisper proactively provides 8 high-quality options**, based on deep understanding of the entire codebase, guessing what you most likely want to do. You just pick a number, and AI continues to dive deeper, progressively refining until it finds what you really want.

### 🚀 Workflow

```
1. Scanning Phase
   └─ Master Agent deploys hundreds/thousands of Sub Agents
      └─ Parallel scan, read, and understand all files in the folder
         └─ Build complete knowledge graph

2. No-Chat Mode (Default)
   └─ Hundreds/thousands of Sub Agents continuously communicate in background
      └─ Guess user needs
         └─ Generate 8 high-quality options + 1 switch to Chat mode option
            └─ User selects an option
               └─ Sub Agents rethink based on selection
                  └─ Generate more refined 8+1 options
                     └─ Iterate, progressively refine to granular level

3. Chat Mode (Optional)
   └─ User freely inputs questions
      └─ AI answers based on complete codebase understanding
         └─ After each answer, provide option to switch back to No-Chat mode
            └─ After switching, Sub Agents regenerate 8+1 options based on conversation
```

### ✨ Core Features

#### 🧠 Intelligent Question Prediction
- **No need to describe problems**: AI proactively guesses what you want
- **Progressive refinement**: From broad direction to specific operations
- **Context-aware**: Dynamically adjusts based on your selection history
- **Dual-mode switching**: No-Chat ↔ Chat seamless transition

#### ⚡ Massive Parallel Scanning
- **Master-Agent Architecture**: One Master coordinates hundreds/thousands of Sub Agents
- **True parallelism**: One Agent per file, maximizing scan speed
- **Multi-AI providers**: Supports 11+ AI providers, automatic load balancing
- **Smart failover**: Automatically switches to backup provider on API failure

#### 🔄 Continuous Background Thinking
- **Sub Agents collaboration**: Continuously communicate in background after scanning
- **Need prediction**: Predict user needs based on codebase characteristics
- **Dynamic adaptation**: Real-time adjustment of prediction strategy based on user choices

#### 🌐 Multi-AI Provider Support
Supports 11+ AI providers, including:
- **International**: Claude (Anthropic), GPT (OpenAI), Gemini (Google), DeepSeek, Mistral, Cohere, HuggingFace
- **Chinese**: GLM (Zhipu), Qwen (Tongyi Qianwen), Moonshot, ERNIE (Wenxin)

### 📦 Quick Start

#### Installation

```bash
# Clone repository
git clone https://github.com/realcarsonterry/CodeWhisper.git
cd CodeWhisper

# Install
pip install -e .
```

#### Configure AI Providers

```bash
# Add one or more AI providers (recommend multiple for auto-failover)
codewhisper add-provider -n anthropic -k YOUR_API_KEY -m claude-opus-4-20250514
codewhisper add-provider -n openai -k YOUR_API_KEY -m gpt-4-turbo
codewhisper add-provider -n glm -k YOUR_API_KEY -m glm-4-plus
```

#### Start Using

```bash
# Navigate to your project directory
cd /path/to/your/project

# Start scanning
codewhisper scan .

# System will:
# 1. Check health status of all configured APIs
# 2. Deploy hundreds/thousands of Sub Agents to scan all files in parallel
# 3. Build knowledge graph
# 4. Enter No-Chat mode, provide 8+1 intelligent options
```

### 🎮 Usage Example

```
Welcome to CodeWhisper!

Scan completed:
- Files: 156
- Analyzed: 156
- Knowledge nodes: 1,247
- Knowledge edges: 3,891

================== No Chat Mode ==================

Based on understanding of the entire codebase, I guess you might want to:

1. Understand overall architecture and module division
2. View authentication and authorization implementation
3. Understand database models and relationships
4. Analyze API interface design
5. Find potential performance bottlenecks
6. Check test coverage
7. View deployment and configuration code
8. Analyze code quality and best practices

9. Switch to Chat mode (free questions)

Please select (1-9): _
```

### 🛠️ Supported AI Providers

| Provider | Get API Key | Recommended Model | Features |
|----------|-------------|-------------------|----------|
| **Anthropic Claude** | [console.anthropic.com](https://console.anthropic.com/) | claude-opus-4-20250514 | Best code understanding |
| **OpenAI** | [platform.openai.com](https://platform.openai.com/api-keys) | gpt-4-turbo | Versatile, fast response |
| **Google Gemini** | [makersuite.google.com](https://makersuite.google.com/app/apikey) | gemini-1.5-pro | Huge context window |
| **DeepSeek** | [platform.deepseek.com](https://platform.deepseek.com/) | deepseek-coder | Code-specific, cost-effective |
| **GLM (Zhipu)** | [open.bigmodel.cn](https://open.bigmodel.cn/) | glm-4-plus | Good Chinese support |
| **Qwen (Tongyi)** | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com/) | qwen-max | Alibaba Cloud ecosystem |
| **Moonshot** | [platform.moonshot.cn](https://platform.moonshot.cn/) | moonshot-v1-128k | Ultra-long context |
| **Mistral** | [console.mistral.ai](https://console.mistral.ai/) | mistral-large-latest | EU privacy-friendly |
| **Cohere** | [dashboard.cohere.com](https://dashboard.cohere.com/) | command-r-plus | Enterprise RAG |
| **ERNIE (Wenxin)** | [console.bce.baidu.com/qianfan](https://console.bce.baidu.com/qianfan/) | ernie-4.0 | Baidu ecosystem |
| **HuggingFace** | [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens) | Any open-source model | Self-hosted, customizable |

### 💰 Cost Optimization Tips

- **Initial scanning**: Use cheap models (DeepSeek, GLM, Qwen)
- **Deep analysis**: Use high-quality models (Claude Opus, GPT-4)
- **Mixed strategy**: Configure multiple providers, automatic load balancing
- **Chinese providers**: GLM, Qwen, Moonshot are extremely cost-effective (~$0.001-0.02/1M tokens)

### ⚠️ Project Status

**This project is currently in early development stage (Alpha)**

- ✅ Core features implemented: parallel scanning, knowledge graph, No-Chat mode
- ⚠️ Many issues and areas for optimization remain
- 🚧 API may change
- 🐛 Undiscovered bugs may exist

**We need your help!**

If you're interested in this project, welcome to:
- 🐛 Report bugs: [Submit Issue](https://github.com/realcarsonterry/CodeWhisper/issues)
- 💡 Suggest ideas: [Join Discussion](https://github.com/realcarsonterry/CodeWhisper/discussions)
- 🔧 Contribute code: [Submit Pull Request](https://github.com/realcarsonterry/CodeWhisper/pulls)
- ⭐ Star this project to help more people discover it

### 🎯 Issues to Resolve

- [ ] Sub Agents continuous background thinking mechanism not fully implemented
- [ ] Question generation quality needs further optimization
- [ ] Performance optimization for large codebases (10,000+ files)
- [ ] Knowledge graph visualization interface
- [ ] Smarter context awareness and need prediction
- [ ] Support for more AI providers
- [ ] Comprehensive test coverage
- [ ] Detailed documentation and tutorials

### 👨‍💻 About the Author

**This project is independently developed by [Terry Carson YM](https://github.com/realcarsonterry).**

This is not an AI-generated project, but a real tool created by a human developer to solve actual code understanding problems.

While AI-assisted coding was used during development, all architectural design, core concepts, and feature planning come from human thinking and creativity.

### 📄 License

MIT License - See [LICENSE](LICENSE) file for details

### 🤝 Contributing

We welcome all forms of contribution! Whether it's:
- Fixing bugs
- Adding new features
- Improving documentation
- Optimizing performance
- Suggesting ideas

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

### 📞 Contact

- **GitHub Issues**: https://github.com/realcarsonterry/CodeWhisper/issues
- **GitHub Discussions**: https://github.com/realcarsonterry/CodeWhisper/discussions

---

<div align="center">

**Let AI guess your needs, instead of making you describe problems**

[⭐ Star](https://github.com/realcarsonterry/CodeWhisper) • [🐛 Report Issue](https://github.com/realcarsonterry/CodeWhisper/issues) • [💡 Feature Request](https://github.com/realcarsonterry/CodeWhisper/discussions)

</div>

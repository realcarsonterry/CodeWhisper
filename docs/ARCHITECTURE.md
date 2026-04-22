# Architecture Documentation

## Overview

No Chat Bot is an AI-powered codebase analysis and recommendation tool designed to help developers understand and explore code repositories through intelligent question-based navigation and contextual chat assistance.

## Design Principles

1. **Modularity**: Each component has a single, well-defined responsibility
2. **Extensibility**: Easy to add new AI providers, scanners, or features
3. **Context Awareness**: All interactions are informed by user history and project knowledge
4. **Privacy First**: User controls what data is accessed and analyzed
5. **Async-First**: Designed for efficient concurrent operations

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     User Interface Layer                     │
│  ┌──────────────┐              ┌──────────────────────────┐ │
│  │  CLI (Click) │              │  Future: Web Interface   │ │
│  └──────────────┘              └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Application Layer                         │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │ Question         │         │ Intelligent Chat Bot     │ │
│  │ Generator        │◄────────┤ (Context-Aware)          │ │
│  └──────────────────┘         └──────────────────────────┘ │
│           │                              │                   │
│           │                              │                   │
│           ▼                              ▼                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Conversation Context Manager                  │  │
│  │  - Selection History  - Chat History                 │  │
│  │  - Mode Switches      - Knowledge Base               │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    AI Provider Layer                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐ │
│  │   Claude     │  │   OpenAI     │  │   DeepSeek       │ │
│  │   Provider   │  │   Provider   │  │   Provider       │ │
│  └──────────────┘  └──────────────┘  └──────────────────┘ │
│           │                │                   │             │
│           └────────────────┴───────────────────┘             │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  AIProvider Base  │                      │
│                  │  (Abstract Class) │                      │
│                  └───────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Scanner Engine Layer                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Master Agent (Orchestrator)              │  │
│  │  - Task Distribution  - Result Aggregation           │  │
│  └──────────────────────────────────────────────────────┘  │
│           │                                                  │
│           ▼                                                  │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   Task Queue                          │  │
│  │  - Priority Queue  - Load Balancing                  │  │
│  └──────────────────────────────────────────────────────┘  │
│           │                                                  │
│           ▼                                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ Sub Agent  │  │ Sub Agent  │  │ Sub Agent  │  ...     │
│  │     #1     │  │     #2     │  │     #N     │          │
│  └────────────┘  └────────────┘  └────────────┘          │
│           │                │                │               │
│           └────────────────┴────────────────┘               │
│                            │                                 │
│                  ┌─────────▼─────────┐                      │
│                  │  File Discovery   │                      │
│                  │  - Git Integration│                      │
│                  │  - Pattern Match  │                      │
│                  └───────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    Storage Layer                             │
│  ┌──────────────────┐         ┌──────────────────────────┐ │
│  │  Configuration   │         │  Knowledge Base          │ │
│  │  (~/.nochatbot)  │         │  (Vector DB - Future)    │ │
│  └──────────────────┘         └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Configuration Manager (`config.py`)

**Responsibility**: Manages application configuration, API keys, and user preferences.

**Key Features**:
- Stores configuration in `~/.nochatbot/config.json`
- Manages multiple AI provider credentials
- Handles scanning preferences and exclusions
- Privacy settings and permissions

**Data Structure**:
```python
{
    "version": "1.0.0",
    "providers": {
        "anthropic": {"api_key": "...", "model": "..."},
        "openai": {"api_key": "...", "model": "..."}
    },
    "scanning": {
        "max_agents": 100,
        "exclude_dirs": [...],
        "exclude_files": [...],
        "max_file_size_mb": 10
    },
    "knowledge_base": {
        "path": "~/.nochatbot/knowledge",
        "vector_db": "chromadb"
    },
    "privacy": {
        "permissions_granted": false,
        "exclude_paths": [...]
    }
}
```

**Key Methods**:
- `add_provider()`: Add/update AI provider configuration
- `grant_permissions()`: Update privacy settings
- `get_scanning_config()`: Retrieve scanning preferences
- `is_permissions_granted()`: Check if user has granted file access

### 2. AI Provider Layer (`providers/`)

**Responsibility**: Provides unified interface for multiple AI providers.

**Architecture Pattern**: Strategy Pattern with Abstract Base Class

**Base Interface** (`base.py`):
```python
class AIProvider(ABC):
    @abstractmethod
    async def send_message(message, system_prompt, temperature, max_tokens) -> str
    
    @abstractmethod
    async def stream_response(message, system_prompt, temperature, max_tokens) -> AsyncIterator[str]
    
    @abstractmethod
    def get_cost_per_token() -> Dict[str, float]
    
    def calculate_cost(input_tokens, output_tokens) -> float
```

**Implementations**:
- `claude.py`: Anthropic Claude provider (Claude Opus 4, Sonnet, etc.)
- `openai.py`: OpenAI provider (GPT-4, GPT-3.5, etc.)
- `deepseek.py`: DeepSeek provider

**Benefits**:
- Easy to add new providers
- Consistent API across all providers
- Built-in cost tracking
- Support for both streaming and non-streaming responses

### 3. Scanner Engine (`scanner/`)

**Responsibility**: Discovers and analyzes codebase structure using multi-agent parallelism.

#### 3.1 File Discovery (`file_discovery.py`)

**Purpose**: Discovers files in the codebase while respecting exclusions.

**Features**:
- Git integration for repository analysis
- Pattern-based file filtering
- Respects `.gitignore` patterns
- Size-based filtering

**Key Methods**:
- `discover_files(path)`: Find all relevant files
- `filter_by_patterns(files, patterns)`: Apply exclusion patterns
- `get_file_metadata(file)`: Extract file information

#### 3.2 Master Agent (`master_agent.py`)

**Purpose**: Orchestrates the scanning process and coordinates sub-agents.

**Responsibilities**:
- Task distribution to sub-agents
- Load balancing across agents
- Result aggregation
- Progress tracking

**Workflow**:
1. Receive scan request
2. Discover files using File Discovery
3. Create tasks for each file/directory
4. Distribute tasks to sub-agents via Task Queue
5. Collect and aggregate results
6. Generate summary report

#### 3.3 Sub Agent (`sub_agent.py`)

**Purpose**: Analyzes individual files or directories.

**Capabilities**:
- Language detection
- Dependency extraction
- Code structure analysis
- Pattern recognition

**Analysis Types**:
- Syntax analysis
- Import/dependency mapping
- Function/class extraction
- Documentation parsing

#### 3.4 Task Queue (`task_queue.py`)

**Purpose**: Manages task distribution and prioritization.

**Features**:
- Priority-based queue
- Load balancing
- Task retry logic
- Concurrent execution control

**Queue Structure**:
```python
Task {
    id: str
    type: TaskType  # FILE_ANALYSIS, DIR_SCAN, etc.
    priority: int
    path: str
    metadata: Dict[str, Any]
    retry_count: int
}
```

### 4. Question Generator (`recommendation/question_generator.py`)

**Responsibility**: Generates intelligent, context-aware questions and options.

**Three Generation Modes**:

#### 4.1 First Time Mode
- **Trigger**: Initial project scan
- **Input**: Project scan results
- **Output**: 8 options covering different project aspects
- **Focus**: Broad exploration of project structure, tech stack, architecture

#### 4.2 Subsequent Mode
- **Trigger**: After user makes selections
- **Input**: Selection history + knowledge base
- **Output**: 8 options for deeper exploration
- **Focus**: Building on previous selections, avoiding repetition

#### 4.3 From Chat Mode
- **Trigger**: Switching back from chat mode
- **Input**: Chat conversation content + knowledge base
- **Output**: 8 options related to chat topics
- **Focus**: Converting abstract discussions into concrete code analysis

**Generation Process**:
```
1. Analyze Context
   ├─ Parse input (scan results / history / chat)
   ├─ Summarize knowledge base
   └─ Identify user interests

2. Build AI Prompt
   ├─ Include context summary
   ├─ Specify generation requirements
   └─ Define output format (JSON)

3. Call AI Provider
   ├─ Send prompt with system instructions
   ├─ Temperature: 0.7 (balanced creativity)
   └─ Max tokens: 2048

4. Parse Response
   ├─ Extract JSON from response
   ├─ Validate structure
   └─ Ensure exactly 8 options

5. Return QuestionResult
   └─ Question + 8 options with descriptions
```

### 5. Conversation Context (`interaction/context.py`)

**Responsibility**: Maintains complete conversation state and history.

**Tracked Information**:
- **Choice History**: All question-answer selections
- **Chat History**: Complete chat conversation
- **Mode Switches**: Transitions between question and chat modes
- **Knowledge Base**: Accumulated project knowledge
- **Current Depth**: How deep user has explored

**Data Structures**:
```python
@dataclass
class ChoiceRecord:
    question: str
    choice: str
    all_options: List[str]
    timestamp: datetime
    depth: int

@dataclass
class ChatMessage:
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime

@dataclass
class ModeSwitch:
    from_mode: str
    to_mode: str
    reason: str
    timestamp: datetime
```

**Key Methods**:
- `add_choice()`: Record user selection
- `add_chat_message()`: Record chat message
- `switch_to_chat()`: Switch to chat mode
- `switch_to_questions()`: Switch to question mode
- `get_context_summary()`: Get complete context for AI

### 6. Intelligent Chat Bot (`interaction/chatbot.py`)

**Responsibility**: Provides context-aware conversational assistance.

**Key Features**:
- **Full Context Awareness**: Knows all user selections and chat history
- **Streaming Support**: Can stream responses token-by-token
- **Knowledge Integration**: Uses accumulated project knowledge
- **Precise Assistance**: Answers based on actual project state

**System Prompt Construction**:
```
1. Role Definition
   └─ "You are an intelligent assistant for No Chat Bot..."

2. User's Selection Path
   ├─ Question 1: [question] → Choice: [choice]
   ├─ Question 2: [question] → Choice: [choice]
   └─ ...

3. Project Information
   ├─ Language: Python
   ├─ Framework: Flask
   └─ ...

4. Knowledge Base Summary
   └─ Relevant information from knowledge base

5. Chat History Context
   └─ Previous conversation summary

6. Instructions
   ├─ Provide precise, helpful responses
   ├─ Reference selections when relevant
   ├─ Be concise but thorough
   └─ Ask clarifying questions if needed
```

**Chat Flow**:
```
User Message
    │
    ▼
Add to Chat History
    │
    ▼
Build System Prompt (with full context)
    │
    ▼
Build Message History (last 10 messages)
    │
    ▼
Call AI Provider
    │
    ├─ Streaming Mode
    │   └─ Yield chunks as they arrive
    │
    └─ Non-Streaming Mode
        └─ Return complete response
    │
    ▼
Add Response to Chat History
    │
    ▼
Return to User
```

## Data Flow

### Scanning Flow

```
User: nochatbot scan /path/to/project
    │
    ▼
CLI validates path and permissions
    │
    ▼
Master Agent initialized
    │
    ▼
File Discovery scans directory
    │
    ├─ Respects .gitignore
    ├─ Applies exclusion patterns
    └─ Filters by file size
    │
    ▼
Tasks created for each file
    │
    ▼
Tasks added to Task Queue
    │
    ▼
Sub Agents pull tasks from queue
    │
    ├─ Agent 1: Analyzes file A
    ├─ Agent 2: Analyzes file B
    └─ Agent N: Analyzes file N
    │
    ▼
Results sent back to Master Agent
    │
    ▼
Master Agent aggregates results
    │
    ├─ File count
    ├─ Language distribution
    ├─ Dependencies
    ├─ Key files
    └─ Project structure
    │
    ▼
Scan results returned to CLI
    │
    ▼
Question Generator creates first question
    │
    ▼
User sees 8 options to explore
```

### Question-Answer Flow

```
User selects option #3
    │
    ▼
Context Manager records choice
    │
    ├─ Question: "What aspect..."
    ├─ Choice: "Analyze core functionality"
    ├─ All options: [1, 2, 3, 4, 5, 6, 7, 8]
    └─ Timestamp: 2026-04-22T10:30:00
    │
    ▼
Knowledge Base updated
    │
    └─ Add information about user's interest
    │
    ▼
Question Generator called
    │
    ├─ Mode: "subsequent"
    ├─ Input: Selection history + KB
    └─ Output: New question + 8 options
    │
    ▼
AI Provider generates options
    │
    ├─ Analyzes previous selections
    ├─ Avoids repetition
    └─ Provides deeper exploration
    │
    ▼
User sees next set of 8 options
```

### Chat Flow

```
User: "How does the config system work?"
    │
    ▼
Context switches to "chat" mode
    │
    ▼
Chat message added to history
    │
    ▼
Chat Bot builds system prompt
    │
    ├─ Include selection history
    ├─ Include project info
    ├─ Include knowledge base
    └─ Include chat history
    │
    ▼
AI Provider called with full context
    │
    ▼
Response generated
    │
    ├─ References user's previous selections
    ├─ Uses project-specific information
    └─ Provides precise answer
    │
    ▼
Response added to chat history
    │
    ▼
User receives contextual answer
```

## Extensibility Points

### Adding a New AI Provider

1. Create new file in `providers/` (e.g., `gemini.py`)
2. Inherit from `AIProvider` base class
3. Implement required methods:
   - `send_message()`
   - `stream_response()`
   - `get_cost_per_token()`
4. Register in `providers/__init__.py`

Example:
```python
from nochatbot.providers.base import AIProvider

class GeminiProvider(AIProvider):
    async def send_message(self, message, system_prompt, temperature, max_tokens):
        # Implementation
        pass
    
    async def stream_response(self, message, system_prompt, temperature, max_tokens):
        # Implementation
        pass
    
    def get_cost_per_token(self):
        return {"input": 0.00001, "output": 0.00003}
```

### Adding a New Scanner Type

1. Create new sub-agent class in `scanner/`
2. Implement analysis logic
3. Register with Master Agent
4. Add task type to Task Queue

### Adding a New Question Mode

1. Add mode to Question Generator
2. Implement `_build_[mode]_prompt()` method
3. Update context tracking
4. Add mode switch logic

## Performance Considerations

### Concurrency

- **Scanner**: Up to 100 concurrent sub-agents (configurable)
- **Task Queue**: Async-first design for efficient I/O
- **AI Calls**: Parallel requests when possible

### Caching

- **Configuration**: Loaded once, cached in memory
- **File Discovery**: Results cached per session
- **Knowledge Base**: Incremental updates (future: vector DB)

### Rate Limiting

- Respect AI provider rate limits
- Implement exponential backoff for retries
- Queue management to prevent overload

## Security Considerations

### API Key Management

- Stored in config file with restricted permissions
- Never logged or exposed in error messages
- Support for environment variables

### File Access

- User must grant explicit permissions
- Configurable exclusion paths
- Respects `.gitignore` patterns
- File size limits to prevent abuse

### Data Privacy

- No data sent to external services except AI providers
- User controls what files are analyzed
- Local-first architecture
- Future: Option for local AI models

## Future Enhancements

### Vector Database Integration

- Store project knowledge in vector DB (ChromaDB, Pinecone)
- Semantic search for relevant context
- Better knowledge retrieval for chat bot

### Web Interface

- Browser-based UI
- Real-time collaboration
- Visual project exploration

### IDE Plugins

- VS Code extension
- JetBrains plugin
- Direct integration with development workflow

### Team Features

- Shared knowledge bases
- Team-wide insights
- Collaborative exploration

## Conclusion

No Chat Bot's architecture is designed for:
- **Modularity**: Easy to understand and modify
- **Extensibility**: Simple to add new features
- **Performance**: Efficient concurrent operations
- **Privacy**: User control over data access
- **Intelligence**: Context-aware assistance

The system combines powerful AI capabilities with thoughtful design to help developers understand and explore codebases effectively.

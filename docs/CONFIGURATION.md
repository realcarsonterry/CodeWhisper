# Configuration Guide

This guide provides comprehensive documentation for configuring No Chat Bot, including all configuration options, file formats, and best practices.

## Table of Contents

- [Configuration File Location](#configuration-file-location)
- [Configuration Structure](#configuration-structure)
- [Provider Configuration](#provider-configuration)
- [Scanning Configuration](#scanning-configuration)
- [Knowledge Base Configuration](#knowledge-base-configuration)
- [Privacy Configuration](#privacy-configuration)
- [Environment Variables](#environment-variables)
- [Configuration Management](#configuration-management)
- [Advanced Configuration](#advanced-configuration)
- [Best Practices](#best-practices)

## Configuration File Location

No Chat Bot stores its configuration in a JSON file at:

- **Linux/macOS**: `~/.codewhisper/config.json`
- **Windows**: `%USERPROFILE%\.codewhisper\config.json`

The configuration directory is created automatically on first run with default settings.

## Configuration Structure

### Complete Configuration Example

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-...",
      "model": "claude-opus-4-20250514"
    },
    "openai": {
      "api_key": "sk-...",
      "model": "gpt-4"
    },
    "deepseek": {
      "api_key": "sk-...",
      "model": "deepseek-chat"
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
      "build",
      ".next",
      "target",
      "bin",
      "obj"
    ],
    "exclude_files": [
      "*.pyc",
      "*.log",
      "*.tmp",
      ".DS_Store",
      "*.swp",
      "*.swo",
      "*.bak"
    ],
    "max_file_size_mb": 10,
    "follow_symlinks": false,
    "respect_gitignore": true
  },
  "knowledge_base": {
    "path": "~/.codewhisper/knowledge",
    "vector_db": "chromadb",
    "max_entries": 10000,
    "embedding_model": "text-embedding-ada-002"
  },
  "privacy": {
    "permissions_granted": true,
    "exclude_paths": [
      "/home/user/secrets",
      "/home/user/.ssh",
      "/home/user/.aws"
    ],
    "anonymize_paths": false,
    "send_telemetry": false
  },
  "ui": {
    "theme": "dark",
    "language": "en",
    "show_cost_estimates": true
  },
  "performance": {
    "cache_enabled": true,
    "cache_ttl_seconds": 3600,
    "request_timeout_seconds": 30,
    "max_retries": 3
  }
}
```

## Provider Configuration

### Supported Providers

No Chat Bot supports multiple AI providers. You can configure one or more providers and switch between them as needed.

#### Anthropic Claude

```json
{
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-...",
      "model": "claude-opus-4-20250514"
    }
  }
}
```

**Available Models**:
- `claude-opus-4-20250514` - Most capable model (recommended)
- `claude-sonnet-4-20250514` - Balanced performance and cost
- `claude-3-5-sonnet-20241022` - Previous generation
- `claude-3-opus-20240229` - Previous generation

**Cost per 1M tokens** (approximate):
- Opus 4: $15 input / $75 output
- Sonnet 4: $3 input / $15 output

#### OpenAI

```json
{
  "providers": {
    "openai": {
      "api_key": "sk-...",
      "model": "gpt-4-turbo-preview"
    }
  }
}
```

**Available Models**:
- `gpt-4-turbo-preview` - Latest GPT-4 Turbo
- `gpt-4` - Standard GPT-4
- `gpt-3.5-turbo` - Faster, more economical

**Cost per 1M tokens** (approximate):
- GPT-4 Turbo: $10 input / $30 output
- GPT-4: $30 input / $60 output
- GPT-3.5 Turbo: $0.50 input / $1.50 output

#### DeepSeek

```json
{
  "providers": {
    "deepseek": {
      "api_key": "sk-...",
      "model": "deepseek-chat"
    }
  }
}
```

**Available Models**:
- `deepseek-chat` - General purpose chat model
- `deepseek-coder` - Specialized for code

### Adding a Provider

#### Using CLI

```bash
# Add Anthropic provider
nochatbot config --provider anthropic --api-key YOUR_KEY --model claude-opus-4-20250514

# Add OpenAI provider
nochatbot config --provider openai --api-key YOUR_KEY --model gpt-4-turbo-preview

# Add DeepSeek provider
nochatbot config --provider deepseek --api-key YOUR_KEY --model deepseek-chat
```

#### Using Python API

```python
from nochatbot.config import Config

config = Config()
config.add_provider(
    name="anthropic",
    api_key="sk-ant-api03-...",
    model="claude-opus-4-20250514"
)
```

#### Manual Configuration

Edit `~/.codewhisper/config.json` and add provider configuration under the `providers` key.

### Removing a Provider

```bash
# Using Python API
from nochatbot.config import Config

config = Config()
config.remove_provider("anthropic")
```

## Scanning Configuration

### Basic Scanning Options

```json
{
  "scanning": {
    "max_agents": 100,
    "exclude_dirs": [...],
    "exclude_files": [...],
    "max_file_size_mb": 10
  }
}
```

### Configuration Options

#### `max_agents`

**Type**: Integer  
**Default**: 100  
**Range**: 1-1000

Maximum number of concurrent scanning agents. Higher values provide faster scanning but consume more resources.

**Recommendations**:
- Small projects (<100 files): 10-20 agents
- Medium projects (100-1000 files): 50-100 agents
- Large projects (>1000 files): 100-200 agents

```bash
# Set via CLI
nochatbot config --max-agents 50
```

#### `exclude_dirs`

**Type**: Array of strings  
**Default**: `["node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"]`

Directories to exclude from scanning. Supports exact matches only (no wildcards).

**Common exclusions**:
```json
{
  "exclude_dirs": [
    "node_modules",      // Node.js dependencies
    ".git",              // Git repository data
    "__pycache__",       // Python cache
    ".venv", "venv",     // Python virtual environments
    "dist", "build",     // Build outputs
    ".next",             // Next.js build
    "target",            // Rust/Java build
    "vendor",            // Go/PHP dependencies
    "coverage",          // Test coverage reports
    ".pytest_cache",     // Pytest cache
    ".mypy_cache",       // MyPy cache
    "bin", "obj"         // .NET build outputs
  ]
}
```

#### `exclude_files`

**Type**: Array of strings  
**Default**: `["*.pyc", "*.log", ".DS_Store"]`

File patterns to exclude from scanning. Supports glob patterns.

**Common exclusions**:
```json
{
  "exclude_files": [
    "*.pyc",             // Python bytecode
    "*.pyo",             // Python optimized bytecode
    "*.log",             // Log files
    "*.tmp",             // Temporary files
    ".DS_Store",         // macOS metadata
    "*.swp", "*.swo",    // Vim swap files
    "*.bak",             // Backup files
    "*.min.js",          // Minified JavaScript
    "*.map",             // Source maps
    "package-lock.json", // NPM lock file
    "yarn.lock",         // Yarn lock file
    "Pipfile.lock"       // Python lock file
  ]
}
```

#### `max_file_size_mb`

**Type**: Integer  
**Default**: 10  
**Range**: 1-100

Maximum file size in megabytes to analyze. Files larger than this are skipped.

**Recommendations**:
- For most projects: 10 MB
- For projects with large data files: 20-50 MB
- To analyze all files: 100 MB (may impact performance)

#### `follow_symlinks`

**Type**: Boolean  
**Default**: false

Whether to follow symbolic links during scanning.

**Warning**: Enabling this may cause infinite loops if symlinks create cycles.

#### `respect_gitignore`

**Type**: Boolean  
**Default**: true

Whether to respect `.gitignore` patterns when scanning.

## Knowledge Base Configuration

```json
{
  "knowledge_base": {
    "path": "~/.codewhisper/knowledge",
    "vector_db": "chromadb",
    "max_entries": 10000,
    "embedding_model": "text-embedding-ada-002"
  }
}
```

### Configuration Options

#### `path`

**Type**: String  
**Default**: `~/.codewhisper/knowledge`

Directory where knowledge base data is stored.

#### `vector_db`

**Type**: String  
**Default**: `chromadb`  
**Options**: `chromadb`, `pinecone`, `weaviate` (future)

Vector database backend for knowledge storage.

#### `max_entries`

**Type**: Integer  
**Default**: 10000

Maximum number of entries to store in knowledge base.

#### `embedding_model`

**Type**: String  
**Default**: `text-embedding-ada-002`

Model to use for generating embeddings (future feature).

## Privacy Configuration

```json
{
  "privacy": {
    "permissions_granted": true,
    "exclude_paths": [
      "/home/user/secrets",
      "/home/user/.ssh"
    ],
    "anonymize_paths": false,
    "send_telemetry": false
  }
}
```

### Configuration Options

#### `permissions_granted`

**Type**: Boolean  
**Default**: false

Whether user has granted permission for file scanning.

**Setting via CLI**:
```bash
# Grant permissions
nochatbot config --grant-permissions

# Revoke permissions
nochatbot config --revoke-permissions
```

#### `exclude_paths`

**Type**: Array of strings  
**Default**: `[]`

Absolute paths to exclude from scanning for privacy/security reasons.

**Common exclusions**:
```json
{
  "exclude_paths": [
    "/home/user/.ssh",           // SSH keys
    "/home/user/.aws",           // AWS credentials
    "/home/user/.gnupg",         // GPG keys
    "/home/user/secrets",        // Secret files
    "/home/user/.env",           // Environment variables
    "/home/user/.config/gcloud"  // Google Cloud credentials
  ]
}
```

**Setting via CLI**:
```bash
nochatbot config --exclude-path /path/to/sensitive/data
```

#### `anonymize_paths`

**Type**: Boolean  
**Default**: false

Whether to anonymize file paths before sending to AI providers (future feature).

#### `send_telemetry`

**Type**: Boolean  
**Default**: false

Whether to send anonymous usage telemetry (future feature).

## Environment Variables

Environment variables take precedence over configuration file settings.

### API Keys

```bash
# Anthropic
export ANTHROPIC_API_KEY='sk-ant-api03-...'

# OpenAI
export OPENAI_API_KEY='sk-...'

# DeepSeek
export DEEPSEEK_API_KEY='sk-...'
```

### Configuration Override

```bash
# Override config file location
export NOCHATBOT_CONFIG_DIR='/custom/path'

# Override default provider
export NOCHATBOT_DEFAULT_PROVIDER='openai'

# Override max agents
export NOCHATBOT_MAX_AGENTS='50'
```

### Loading from .env File

Create a `.env` file in your project directory:

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-api03-...
OPENAI_API_KEY=sk-...
NOCHATBOT_MAX_AGENTS=50
```

No Chat Bot automatically loads `.env` files using `python-dotenv`.

## Configuration Management

### View Current Configuration

```bash
# Using CLI (future feature)
nochatbot config --show

# Using Python API
from nochatbot.config import Config

config = Config()
print(config.config)
```

### Reset to Defaults

```bash
# Using Python API
from nochatbot.config import Config

config = Config()
config.config = config.get_default_config()
config.save_config()
```

### Backup Configuration

```bash
# Linux/macOS
cp ~/.codewhisper/config.json ~/.codewhisper/config.json.backup

# Windows
copy %USERPROFILE%\.codewhisper\config.json %USERPROFILE%\.codewhisper\config.json.backup
```

### Restore Configuration

```bash
# Linux/macOS
cp ~/.codewhisper/config.json.backup ~/.codewhisper/config.json

# Windows
copy %USERPROFILE%\.codewhisper\config.json.backup %USERPROFILE%\.codewhisper\config.json
```

## Advanced Configuration

### Multiple Profiles

Create multiple configuration profiles for different use cases:

```bash
# Development profile
export NOCHATBOT_CONFIG_DIR=~/.codewhisper-dev

# Production profile
export NOCHATBOT_CONFIG_DIR=~/.codewhisper-prod
```

### Project-Specific Configuration

Create a `.codewhisper.json` file in your project root:

```json
{
  "scanning": {
    "exclude_dirs": ["custom_dir"],
    "max_agents": 20
  }
}
```

Project-specific settings override global configuration.

### Custom Exclusion Patterns

Create a `.codewhisperignore` file (similar to `.gitignore`):

```
# Ignore all log files
*.log

# Ignore specific directories
temp/
cache/

# Ignore files matching pattern
*_backup.*
```

## Best Practices

### Security

1. **Never commit API keys** to version control
2. **Use environment variables** for sensitive data
3. **Set appropriate exclude_paths** for sensitive directories
4. **Regularly rotate API keys**
5. **Use separate keys** for development and production

### Performance

1. **Adjust max_agents** based on system resources
2. **Exclude large directories** (node_modules, build outputs)
3. **Set reasonable max_file_size_mb** limits
4. **Enable caching** for repeated scans
5. **Use faster models** (Sonnet instead of Opus) for quick scans

### Cost Optimization

1. **Choose appropriate models** for your use case
2. **Monitor token usage** with cost estimates
3. **Use cheaper models** for initial exploration
4. **Cache results** to avoid redundant API calls
5. **Set max_tokens limits** in provider configuration

### Organization

1. **Use descriptive provider names** if configuring multiple accounts
2. **Document custom exclusions** in comments (future feature)
3. **Keep configuration backed up**
4. **Use version control** for project-specific configs
5. **Review and update** exclusion patterns regularly

## Configuration Examples

### Minimal Configuration

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-..."
    }
  }
}
```

### Development Configuration

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-...",
      "model": "claude-sonnet-4-20250514"
    }
  },
  "scanning": {
    "max_agents": 20,
    "exclude_dirs": ["node_modules", ".git", "dist", "coverage"]
  },
  "privacy": {
    "permissions_granted": true,
    "exclude_paths": ["/home/dev/.env", "/home/dev/secrets"]
  }
}
```

### Production Configuration

```json
{
  "version": "1.0.0",
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-...",
      "model": "claude-opus-4-20250514"
    }
  },
  "scanning": {
    "max_agents": 100,
    "exclude_dirs": ["node_modules", ".git", "dist", "build", "vendor"],
    "max_file_size_mb": 20
  },
  "privacy": {
    "permissions_granted": true,
    "exclude_paths": [
      "/app/.env",
      "/app/secrets",
      "/app/.aws"
    ]
  },
  "performance": {
    "cache_enabled": true,
    "cache_ttl_seconds": 7200,
    "request_timeout_seconds": 60
  }
}
```

## Troubleshooting

### Configuration Not Loading

1. Check file location: `~/.codewhisper/config.json`
2. Verify JSON syntax (use a JSON validator)
3. Check file permissions (must be readable)
4. Look for error messages in logs

### API Key Not Working

1. Verify key format (starts with correct prefix)
2. Check for extra spaces or newlines
3. Ensure key has not expired
4. Test key with provider's API directly

### Scanning Too Slow

1. Reduce `max_agents` if system is overloaded
2. Add more directories to `exclude_dirs`
3. Reduce `max_file_size_mb`
4. Enable caching

### Files Not Being Scanned

1. Check `exclude_dirs` and `exclude_files`
2. Verify `respect_gitignore` setting
3. Check file size against `max_file_size_mb`
4. Review `exclude_paths` in privacy settings

## Additional Resources

- [Installation Guide](INSTALLATION.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [Main README](../README.md)
- [Contributing Guide](../CONTRIBUTING.md)

# Installation Guide

This guide provides detailed installation instructions for No Chat Bot across different platforms and environments.

## Table of Contents

- [System Requirements](#system-requirements)
- [Quick Installation](#quick-installation)
- [Platform-Specific Instructions](#platform-specific-instructions)
- [Installation Methods](#installation-methods)
- [Post-Installation Setup](#post-installation-setup)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Upgrading](#upgrading)
- [Uninstallation](#uninstallation)

## System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum, 2 GB recommended
- **Disk Space**: 100 MB for installation, additional space for knowledge base
- **Internet**: Required for AI API calls
- **Operating System**: 
  - Linux (Ubuntu 20.04+, Debian 10+, Fedora 33+, etc.)
  - macOS 10.15 (Catalina) or higher
  - Windows 10 or higher

### Required Software

- Python 3.8+ with pip
- Git (optional, for development installation)
- Virtual environment tool (recommended)

### API Requirements

At least one of the following:
- Anthropic API key (for Claude models)
- OpenAI API key (for GPT models)
- DeepSeek API key (for DeepSeek models)

## Quick Installation

### For Most Users

```bash
# Install from PyPI (when published)
pip install nochatbot

# Or install from source
git clone https://github.com/yourusername/nochatbot.git
cd nochatbot
pip install -e .
```

### Set Up API Key

```bash
# Linux/macOS
export ANTHROPIC_API_KEY='your-api-key-here'

# Windows (Command Prompt)
set ANTHROPIC_API_KEY=your-api-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY='your-api-key-here'
```

### Verify Installation

```bash
nochatbot --version
```

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt update

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv git

# Create virtual environment
python3 -m venv nochatbot-env
source nochatbot-env/bin/activate

# Install No Chat Bot
pip install nochatbot

# Or from source
git clone https://github.com/yourusername/nochatbot.git
cd nochatbot
pip install -e .
```

#### Fedora/RHEL/CentOS

```bash
# Install Python 3 and pip
sudo dnf install python3 python3-pip git

# Create virtual environment
python3 -m venv nochatbot-env
source nochatbot-env/bin/activate

# Install No Chat Bot
pip install nochatbot
```

#### Arch Linux

```bash
# Install Python and pip
sudo pacman -S python python-pip git

# Create virtual environment
python -m venv nochatbot-env
source nochatbot-env/bin/activate

# Install No Chat Bot
pip install nochatbot
```

### macOS

#### Using Homebrew (Recommended)

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Create virtual environment
python3 -m venv nochatbot-env
source nochatbot-env/bin/activate

# Install No Chat Bot
pip install nochatbot
```

#### Using System Python

```bash
# macOS comes with Python, but install pip if needed
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

# Create virtual environment
python3 -m venv nochatbot-env
source nochatbot-env/bin/activate

# Install No Chat Bot
pip install nochatbot
```

### Windows

#### Using Python Installer

1. **Download Python**:
   - Visit https://www.python.org/downloads/
   - Download Python 3.8 or higher
   - Run installer
   - **Important**: Check "Add Python to PATH" during installation

2. **Open Command Prompt or PowerShell**:
   ```cmd
   # Verify Python installation
   python --version
   pip --version
   ```

3. **Create Virtual Environment**:
   ```cmd
   # Command Prompt
   python -m venv nochatbot-env
   nochatbot-env\Scripts\activate

   # PowerShell
   python -m venv nochatbot-env
   .\nochatbot-env\Scripts\Activate.ps1
   ```

4. **Install No Chat Bot**:
   ```cmd
   pip install nochatbot
   ```

#### Using Windows Subsystem for Linux (WSL)

```bash
# Install WSL if not already installed
wsl --install

# Follow Linux (Ubuntu) instructions above
```

#### Using Anaconda

```bash
# Create conda environment
conda create -n nochatbot python=3.10
conda activate nochatbot

# Install No Chat Bot
pip install nochatbot
```

## Installation Methods

### Method 1: Install from PyPI (Recommended)

```bash
# Install latest stable version
pip install nochatbot

# Install specific version
pip install nochatbot==0.1.0

# Upgrade to latest version
pip install --upgrade nochatbot
```

### Method 2: Install from Source (Development)

```bash
# Clone repository
git clone https://github.com/yourusername/nochatbot.git
cd nochatbot

# Install in editable mode
pip install -e .

# Install with development dependencies
pip install -e ".[dev]"
```

### Method 3: Install from GitHub Release

```bash
# Install from specific release
pip install https://github.com/yourusername/nochatbot/archive/v0.1.0.tar.gz

# Install from main branch
pip install git+https://github.com/yourusername/nochatbot.git
```

### Method 4: Install from Wheel

```bash
# Download wheel file from releases
# Then install
pip install nochatbot-0.1.0-py3-none-any.whl
```

## Post-Installation Setup

### 1. Configure API Keys

#### Option A: Environment Variables (Temporary)

```bash
# Linux/macOS
export ANTHROPIC_API_KEY='sk-ant-...'
export OPENAI_API_KEY='sk-...'

# Windows Command Prompt
set ANTHROPIC_API_KEY=sk-ant-...
set OPENAI_API_KEY=sk-...

# Windows PowerShell
$env:ANTHROPIC_API_KEY='sk-ant-...'
$env:OPENAI_API_KEY='sk-...'
```

#### Option B: Configuration File (Persistent)

```bash
# Use the config command
nochatbot config --provider anthropic --api-key YOUR_API_KEY

# Or manually edit config file
# Linux/macOS: ~/.nochatbot/config.json
# Windows: %USERPROFILE%\.nochatbot\config.json
```

#### Option C: .env File (Development)

```bash
# Create .env file in your project directory
echo "ANTHROPIC_API_KEY=your-key-here" > .env
echo "OPENAI_API_KEY=your-key-here" >> .env
```

### 2. Grant Permissions

```bash
# Grant file scanning permissions
nochatbot config --grant-permissions

# Add exclusion paths for sensitive data
nochatbot config --exclude-path /path/to/sensitive/data
```

### 3. Verify Configuration

```bash
# Check configuration
nochatbot config --show

# Test with a simple scan
nochatbot scan /path/to/test/project
```

## Verification

### Check Installation

```bash
# Check version
nochatbot --version

# Check help
nochatbot --help

# List available commands
nochatbot
```

### Run Tests

```bash
# If installed from source with dev dependencies
pytest

# Run specific test
pytest tests/test_config.py

# Run with coverage
pytest --cov=nochatbot
```

### Test API Connection

```bash
# Create a test script
cat > test_api.py << 'EOF'
import asyncio
from nochatbot.providers import ClaudeProvider

async def test():
    provider = ClaudeProvider(
        api_key="your-key-here",
        model="claude-opus-4-20250514"
    )
    response = await provider.send_message("Hello, world!")
    print(response)

asyncio.run(test())
EOF

# Run test
python test_api.py
```

## Troubleshooting

### Common Issues

#### Issue: "command not found: nochatbot"

**Solution**:
```bash
# Ensure pip bin directory is in PATH
# Linux/macOS
export PATH="$HOME/.local/bin:$PATH"

# Or use python -m
python -m nochatbot --version

# Or reinstall with --user flag
pip install --user nochatbot
```

#### Issue: "No module named 'nochatbot'"

**Solution**:
```bash
# Verify installation
pip list | grep nochatbot

# Reinstall
pip uninstall nochatbot
pip install nochatbot

# Check Python path
python -c "import sys; print(sys.path)"
```

#### Issue: "Permission denied" on Linux/macOS

**Solution**:
```bash
# Install for user only (no sudo needed)
pip install --user nochatbot

# Or use virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate
pip install nochatbot
```

#### Issue: "SSL Certificate Error"

**Solution**:
```bash
# Update certificates
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# Linux
sudo apt install ca-certificates
sudo update-ca-certificates

# Or use pip with trusted host (not recommended)
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org nochatbot
```

#### Issue: "API Key Invalid"

**Solution**:
```bash
# Verify API key format
# Anthropic: starts with "sk-ant-"
# OpenAI: starts with "sk-"

# Check environment variable
echo $ANTHROPIC_API_KEY

# Reconfigure
nochatbot config --provider anthropic --api-key YOUR_KEY
```

#### Issue: "Python version too old"

**Solution**:
```bash
# Check Python version
python --version

# Install newer Python
# Ubuntu/Debian
sudo apt install python3.10

# macOS
brew install python@3.10

# Update alternatives (Linux)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1
```

#### Issue: "ImportError: cannot import name 'X'"

**Solution**:
```bash
# Update dependencies
pip install --upgrade -r requirements.txt

# Or reinstall with force
pip install --force-reinstall nochatbot
```

### Platform-Specific Issues

#### Windows: "Execution Policy" Error (PowerShell)

```powershell
# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Windows: "UnicodeDecodeError"

```cmd
# Set UTF-8 encoding
set PYTHONIOENCODING=utf-8

# Or in Python script
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

#### macOS: "xcrun: error: invalid active developer path"

```bash
# Install Xcode Command Line Tools
xcode-select --install
```

### Getting Help

If you encounter issues not covered here:

1. Check the [GitHub Issues](https://github.com/yourusername/nochatbot/issues)
2. Search for similar problems
3. Create a new issue with:
   - Operating system and version
   - Python version (`python --version`)
   - Installation method used
   - Complete error message
   - Steps to reproduce

## Upgrading

### Upgrade from PyPI

```bash
# Upgrade to latest version
pip install --upgrade nochatbot

# Upgrade to specific version
pip install --upgrade nochatbot==0.2.0
```

### Upgrade from Source

```bash
# Navigate to repository
cd nochatbot

# Pull latest changes
git pull origin main

# Reinstall
pip install -e .
```

### Migration Notes

When upgrading between major versions, check the [CHANGELOG](../CHANGELOG.md) for breaking changes and migration guides.

## Uninstallation

### Remove Package

```bash
# Uninstall No Chat Bot
pip uninstall nochatbot

# Confirm removal
y
```

### Remove Configuration

```bash
# Linux/macOS
rm -rf ~/.nochatbot

# Windows Command Prompt
rmdir /s %USERPROFILE%\.nochatbot

# Windows PowerShell
Remove-Item -Recurse -Force $env:USERPROFILE\.nochatbot
```

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
# Linux/macOS
rm -rf nochatbot-env

# Windows
rmdir /s nochatbot-env
```

## Next Steps

After successful installation:

1. Read the [Quick Start Guide](../README.md#quick-start)
2. Review [Configuration Options](CONFIGURATION.md)
3. Explore [Usage Examples](../examples/)
4. Check out the [Architecture Documentation](ARCHITECTURE.md)

## Additional Resources

- [Official Documentation](../README.md)
- [Configuration Guide](CONFIGURATION.md)
- [Architecture Overview](ARCHITECTURE.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [GitHub Repository](https://github.com/yourusername/nochatbot)
- [Issue Tracker](https://github.com/yourusername/nochatbot/issues)

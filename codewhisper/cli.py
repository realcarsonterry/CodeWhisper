"""Command-line interface for CodeWhisper."""

import click
import sys
import os
from pathlib import Path
from typing import Optional
from codewhisper.config import Config
from codewhisper.providers import (
    ClaudeProvider, OpenAIProvider, DeepSeekProvider, GLMProvider,
    GeminiProvider, CohereProvider, MistralProvider, QwenProvider,
    MoonshotProvider, ERNIEProvider, HuggingFaceProvider
)

# Fix Windows encoding issues
if sys.platform == 'win32':
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8')


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """CodeWhisper - Zero-barrier AI assistant for intelligent codebase understanding.

    A smart assistant that scans your codebase, builds a knowledge base,
    and provides intelligent recommendations through interactive chat.
    """
    pass


@cli.command()
def init():
    """Initialize CodeWhisper configuration.

    Creates the configuration directory and file with default settings.
    This is automatically done on first use, but you can run this command
    to reset your configuration to defaults.
    """
    try:
        config = Config()
        click.echo(click.style("✓ Configuration initialized successfully!", fg="green"))
        click.echo(f"\nConfiguration location: {config.CONFIG_FILE}")
        click.echo("\nNext steps:")
        click.echo("  1. Add an AI provider: nochatbot add-provider")
        click.echo("  2. Scan a directory: nochatbot scan /path/to/project")
    except Exception as e:
        click.echo(click.style(f"✗ Error initializing configuration: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.option('--name', '-n', required=True,
              type=click.Choice(['anthropic', 'openai', 'deepseek', 'glm', 'gemini', 'cohere', 'mistral', 'qwen', 'moonshot', 'ernie', 'huggingface'], case_sensitive=False),
              help='Provider name')
@click.option('--api-key', '-k', required=True,
              help='API key for the provider')
@click.option('--model', '-m',
              help='Default model to use (optional)')
def add_provider(name: str, api_key: str, model: Optional[str]):
    """Add or update an AI provider configuration.

    Examples:
        nochatbot add-provider -n anthropic -k sk-ant-xxx -m claude-opus-4-20250514
        nochatbot add-provider -n openai -k sk-xxx -m gpt-4
        nochatbot add-provider -n deepseek -k sk-xxx
        nochatbot add-provider -n glm -k xxx.yyy -m glm-4-plus
    """
    try:
        config = Config()
        config.add_provider(name.lower(), api_key, model)

        click.echo(click.style(f"✓ Provider '{name}' added successfully!", fg="green"))
        if model:
            click.echo(f"  Model: {model}")
        click.echo(f"\nConfiguration saved to: {config.CONFIG_FILE}")

    except ValueError as e:
        click.echo(click.style(f"✗ Invalid input: {e}", fg="red"), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"✗ Error adding provider: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
@click.argument('path', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.option('--provider', '-p',
              help='Specific provider to use (default: use all configured providers)')
@click.option('--max-agents', '-a', default=1000,
              help='Maximum number of parallel agents (default: 1000, one per file for maximum speed)')
@click.option('--no-interactive', is_flag=True,
              help='Skip interactive interface after scanning')
def scan(path: str, provider: Optional[str], max_agents: int, no_interactive: bool):
    """Scan a directory and build knowledge base.

    This command will:
      1. Check permissions (first-time authorization required)
      2. Load configured AI providers
      3. Scan the directory using parallel agents (one agent per file!)
      4. Build a knowledge graph
      5. Launch interactive chat interface (unless --no-interactive)

    Examples:
        codewhisper scan /path/to/project
        codewhisper scan . --provider glm
        codewhisper scan ~/code/myapp --max-agents 500
    """
    try:
        config = Config()

        # Convert path to absolute
        scan_path = Path(path).resolve()

        click.echo(click.style(f"\nCodeWhisper - Codebase Scanner", fg="cyan", bold=True))
        click.echo(f"Target: {scan_path}\n")

        # Check permissions
        if not _check_permissions(config, scan_path):
            click.echo(click.style("\n✗ Permission denied by user", fg="red"))
            sys.exit(1)

        # Load providers
        providers = _load_providers(config, provider)
        if not providers:
            click.echo(click.style("\n✗ No AI providers configured", fg="red"))
            click.echo("\nPlease add a provider first:")
            click.echo("  nochatbot add-provider -n anthropic -k YOUR_API_KEY")
            sys.exit(1)

        click.echo(click.style(f"\n✓ Loaded {len(providers)} provider(s)", fg="green"))

        # Import here to avoid circular dependencies
        from codewhisper.scanner.master_agent import MasterAgent

        # Get scanning configuration
        scan_config = config.get_scanning_config()

        # Create master agent
        click.echo("\nInitializing master agent...")
        master = MasterAgent(
            providers=providers,
            exclude_dirs=scan_config.get('exclude_dirs', []),
            exclude_files=scan_config.get('exclude_files', []),
            max_file_size_mb=scan_config.get('max_file_size_mb', 10.0)
        )

        # Scan directory
        click.echo(click.style("\nScanning directory...", fg="cyan"))
        results = master.scan_directory(
            path=str(scan_path),
            max_agents=max_agents,
            show_progress=True
        )

        # Build knowledge graph
        click.echo(click.style("\nBuilding knowledge graph...", fg="cyan"))
        import time
        start_time = time.time()
        knowledge_graph = master.build_knowledge_graph()
        elapsed = time.time() - start_time
        click.echo(click.style(f"Knowledge graph built in {elapsed:.2f}s", fg="green"))

        # Display results
        click.echo(click.style("\n" + "="*60, fg="cyan"))
        click.echo(click.style("Scan Results", fg="cyan", bold=True))
        click.echo(click.style("="*60, fg="cyan"))
        click.echo(f"Files scanned:     {results['files_scanned']}")
        click.echo(f"Files analyzed:    {results['files_analyzed']}")
        click.echo(f"Errors:            {results['errors']}")
        click.echo(f"Knowledge nodes:   {knowledge_graph['metadata']['total_nodes']}")
        click.echo(f"Knowledge edges:   {knowledge_graph['metadata']['total_edges']}")

        if results['errors'] > 0:
            click.echo(click.style(f"\n⚠ {results['errors']} file(s) failed to analyze", fg="yellow"))

        # Launch interactive interface
        if not no_interactive:
            click.echo(click.style("\n" + "="*60, fg="cyan"))
            click.echo(click.style("Starting Interactive Interface", fg="cyan", bold=True))
            click.echo(click.style("="*60, fg="cyan"))
            click.echo("\nType 'help' for available commands, 'exit' to quit\n")

            _start_interactive_interface(master, providers[0], scan_path)
        else:
            click.echo(click.style("\n✓ Scan completed successfully!", fg="green"))

    except KeyboardInterrupt:
        click.echo(click.style("\n\n✗ Scan interrupted by user", fg="yellow"))
        sys.exit(130)
    except Exception as e:
        click.echo(click.style(f"\n✗ Error during scan: {e}", fg="red"), err=True)
        import traceback
        if '--debug' in sys.argv:
            traceback.print_exc()
        sys.exit(1)


@cli.command()
def status():
    """Show current configuration status.

    Displays information about:
      - Configuration file location
      - Configured AI providers
      - Scanning settings
      - Privacy settings
    """
    try:
        config = Config()

        click.echo(click.style("\nCodeWhisper - Status", fg="cyan", bold=True))
        click.echo(click.style("="*60, fg="cyan"))

        # Configuration file
        click.echo(f"\nConfiguration: {config.CONFIG_FILE}")
        click.echo(f"Version: {config.config.get('version', 'unknown')}")

        # Providers
        providers = config.get_providers()
        click.echo(click.style(f"\nAI Providers ({len(providers)}):", fg="cyan"))
        if providers:
            for name, provider_config in providers.items():
                model = provider_config.get('model', 'default')
                api_key_preview = provider_config.get('api_key', '')[:10] + '...'
                click.echo(f"  • {name}")
                click.echo(f"    Model: {model}")
                click.echo(f"    API Key: {api_key_preview}")
        else:
            click.echo("  (none configured)")
            click.echo("\n  Add a provider: nochatbot add-provider -n anthropic -k YOUR_KEY")

        # Scanning settings
        scan_config = config.get_scanning_config()
        click.echo(click.style("\nScanning Settings:", fg="cyan"))
        click.echo(f"  Max agents: {scan_config.get('max_agents', 100)}")
        click.echo(f"  Max file size: {scan_config.get('max_file_size_mb', 10)} MB")
        click.echo(f"  Excluded directories: {len(scan_config.get('exclude_dirs', []))}")
        click.echo(f"  Excluded file patterns: {len(scan_config.get('exclude_files', []))}")

        # Privacy settings
        privacy_config = config.get_privacy_config()
        permissions = privacy_config.get('permissions_granted', False)
        click.echo(click.style("\nPrivacy Settings:", fg="cyan"))
        status_color = "green" if permissions else "yellow"
        status_text = "Granted" if permissions else "Not granted"
        click.echo(f"  Permissions: {click.style(status_text, fg=status_color)}")

        excluded_paths = privacy_config.get('exclude_paths', [])
        if excluded_paths:
            click.echo(f"  Excluded paths: {len(excluded_paths)}")
            for path in excluded_paths[:5]:
                click.echo(f"    • {path}")
            if len(excluded_paths) > 5:
                click.echo(f"    ... and {len(excluded_paths) - 5} more")

        # Knowledge base
        kb_config = config.get_knowledge_base_config()
        click.echo(click.style("\nKnowledge Base:", fg="cyan"))
        click.echo(f"  Path: {kb_config.get('path', 'not set')}")
        click.echo(f"  Vector DB: {kb_config.get('vector_db', 'not set')}")

        click.echo()

    except Exception as e:
        click.echo(click.style(f"✗ Error reading status: {e}", fg="red"), err=True)
        sys.exit(1)


@cli.command()
def list_providers():
    """List all configured AI providers.

    Shows detailed information about each configured provider including
    the model being used and a preview of the API key.
    """
    try:
        config = Config()
        providers = config.get_providers()

        if not providers:
            click.echo(click.style("\nNo providers configured.", fg="yellow"))
            click.echo("\nAdd a provider with:")
            click.echo("  nochatbot add-provider -n anthropic -k YOUR_API_KEY")
            return

        click.echo(click.style(f"\nConfigured Providers ({len(providers)}):", fg="cyan", bold=True))
        click.echo(click.style("="*60, fg="cyan"))

        for name, provider_config in providers.items():
            click.echo(f"\n{click.style(name.upper(), fg='green', bold=True)}")

            model = provider_config.get('model', 'default model')
            click.echo(f"  Model:   {model}")

            api_key = provider_config.get('api_key', '')
            if len(api_key) > 15:
                api_key_preview = api_key[:8] + '...' + api_key[-4:]
            else:
                api_key_preview = api_key[:10] + '...'
            click.echo(f"  API Key: {api_key_preview}")

        click.echo()

    except Exception as e:
        click.echo(click.style(f"✗ Error listing providers: {e}", fg="red"), err=True)
        sys.exit(1)


def _check_permissions(config: Config, path: Path) -> bool:
    """Check and request permissions if needed.

    Args:
        config: Configuration instance
        path: Path to be scanned

    Returns:
        True if permissions granted, False otherwise
    """
    if config.is_permissions_granted():
        return True

    click.echo(click.style("\n" + "="*60, fg="yellow"))
    click.echo(click.style("PERMISSION REQUEST", fg="yellow", bold=True))
    click.echo(click.style("="*60, fg="yellow"))

    click.echo("\nCodeWhisper needs permission to scan your codebase.")
    click.echo("\nWhat will be read:")
    click.echo("  • Source code files in the specified directory")
    click.echo("  • File structure and organization")
    click.echo("  • Code content for analysis")

    click.echo("\nHow data will be processed:")
    click.echo("  • Files are sent to configured AI providers for analysis")
    click.echo("  • Analysis results are stored locally in ~/.codewhisper/")
    click.echo("  • No data is stored on external servers except during API calls")
    click.echo("  • You can exclude specific paths from scanning")

    click.echo("\nExcluded by default:")
    scan_config = config.get_scanning_config()
    for excluded in scan_config.get('exclude_dirs', [])[:5]:
        click.echo(f"  • {excluded}/")

    click.echo(click.style("\n" + "="*60, fg="yellow"))

    if click.confirm("\nDo you grant permission to scan this directory?", default=False):
        config.grant_permissions(granted=True)
        click.echo(click.style("\n✓ Permissions granted and saved", fg="green"))
        return True

    return False


def _load_providers(config: Config, provider_name: Optional[str] = None):
    """Load AI providers from configuration.

    Args:
        config: Configuration instance
        provider_name: Optional specific provider to load

    Returns:
        List of initialized provider instances
    """
    providers = []
    provider_configs = config.get_providers()

    if not provider_configs:
        return providers

    # If specific provider requested, only load that one
    if provider_name:
        provider_config = provider_configs.get(provider_name.lower())
        if not provider_config:
            click.echo(click.style(f"✗ Provider '{provider_name}' not found in configuration", fg="red"))
            return providers
        provider_configs = {provider_name.lower(): provider_config}

    for name, provider_config in provider_configs.items():
        try:
            api_key = provider_config.get('api_key')
            model = provider_config.get('model')

            if name == 'anthropic':
                provider = ClaudeProvider(
                    api_key=api_key,
                    model=model or 'claude-opus-4-20250514'
                )
            elif name == 'openai':
                provider = OpenAIProvider(
                    api_key=api_key,
                    model=model or 'gpt-4'
                )
            elif name == 'deepseek':
                provider = DeepSeekProvider(
                    api_key=api_key,
                    model=model or 'deepseek-chat'
                )
            elif name == 'glm':
                provider = GLMProvider(
                    api_key=api_key,
                    model=model or 'glm-4-plus'
                )
            elif name == 'gemini':
                provider = GeminiProvider(
                    api_key=api_key,
                    model=model or 'gemini-1.5-pro'
                )
            elif name == 'cohere':
                provider = CohereProvider(
                    api_key=api_key,
                    model=model or 'command-r-plus'
                )
            elif name == 'mistral':
                provider = MistralProvider(
                    api_key=api_key,
                    model=model or 'mistral-large-latest'
                )
            elif name == 'qwen':
                provider = QwenProvider(
                    api_key=api_key,
                    model=model or 'qwen-max'
                )
            elif name == 'moonshot':
                provider = MoonshotProvider(
                    api_key=api_key,
                    model=model or 'moonshot-v1-32k'
                )
            elif name == 'ernie':
                provider = ERNIEProvider(
                    api_key=api_key,
                    model=model or 'ernie-4.0'
                )
            elif name == 'huggingface':
                provider = HuggingFaceProvider(
                    api_key=api_key,
                    model=model or 'meta-llama/Meta-Llama-3-70B-Instruct'
                )
            else:
                click.echo(click.style(f"⚠ Unknown provider: {name}", fg="yellow"))
                continue

            providers.append(provider)
            click.echo(f"  • {name} ({provider.model})")

        except Exception as e:
            click.echo(click.style(f"⚠ Failed to load provider '{name}': {e}", fg="yellow"))

    return providers


def _start_interactive_interface(master_agent, provider, scan_path: Path):
    """Start the interactive No Chat interface.

    Args:
        master_agent: MasterAgent instance with scan results
        provider: AI provider to use for generating questions
        scan_path: Path that was scanned
    """
    from codewhisper.interaction.interface import InteractiveInterface
    import uuid

    # Get scan results
    results = master_agent.get_results()
    knowledge_graph = master_agent.get_knowledge_graph()

    # Prepare project info
    project_info = {
        'project_name': scan_path.name,
        'project_path': str(scan_path),
        'files_scanned': len(results),
        'files_analyzed': sum(1 for r in results.values() if r.get('status') == 'success'),
        'knowledge_nodes': knowledge_graph['metadata']['total_nodes'],
        'knowledge_edges': knowledge_graph['metadata']['total_edges'],
        'scan_results': results,
        'knowledge_graph': knowledge_graph
    }

    # Create and start interactive interface
    click.echo("\n" + "="*60)
    click.echo(click.style("🎉 Scan Complete! No Chat Mode Ready", fg="green", bold=True))
    click.echo("="*60)
    click.echo("\nCodeWhisper will now present you with 8 intelligent questions.")
    click.echo("Simply choose a number (1-8) or 9 to switch to Chat mode.\n")

    session_id = str(uuid.uuid4())
    interface = InteractiveInterface(
        ai_provider=provider,
        project_info=project_info,
        session_id=session_id
    )

    # Start the No Chat interface
    interface.start()


if __name__ == '__main__':
    cli()

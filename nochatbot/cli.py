"""Command-line interface for No Chat Bot."""

import click
from nochatbot.config import Config


@click.group()
@click.version_option()
def cli():
    """No Chat Bot - AI-powered codebase analysis and recommendation tool."""
    pass


@cli.command()
@click.argument('path', type=click.Path(exists=True))
@click.option('--provider', type=click.Choice(['anthropic', 'openai']), default='anthropic')
def scan(path, provider):
    """Scan a codebase and generate recommendations."""
    click.echo(f"Scanning {path} with {provider} provider...")


if __name__ == '__main__':
    cli()

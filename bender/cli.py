import click

from .jira.cli import cli as jira_cli
from .utils import config_file


@click.group('cli')
def cli():
    """Bending Atlassian to its will since 2020!"""
    pass


@cli.command('config')
def cli_config():
    """show configuration file"""
    print('{}'.format(config_file))


cli.add_command(jira_cli)

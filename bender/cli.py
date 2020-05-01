import os

import click

from bender import APP_VERSION, APP_NAME
from bender.jira.cli import cli as jira_cli
from bender.utils import config, config_file


@click.group('cli')
@click.version_option(f'{APP_VERSION}', prog_name=APP_NAME)
def cli():
    """Bending Atlassian to its will since 2020!"""
    pass


@cli.command('config', no_args_is_help=True)
@click.option('--edit', is_flag=True, default=False, help="edit config file")
@click.option('--create', is_flag=True, default=False, help="create config file")
@click.option('--delete', is_flag=True, default=False, help="delete config file")
def cli_config(edit, delete, create):
    """Manage bender config."""
    if delete:
        os.unlink(config_file)

    if create:
        with click.open_file(config_file, 'w') as f:
            config.write(f)

    if edit:
        click.edit(filename=config_file)

    click.echo(click.format_filename('{}'.format(config_file)))


cli.add_command(jira_cli)

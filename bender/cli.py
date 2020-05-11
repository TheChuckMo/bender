import os

import click

from bender import APP_VERSION, APP_NAME, config_file, local_config_file, config
from bender.confluence.cli import cli as confluence_cli
from bender.crowd.cli import cli as crowd_cli
from bender.jira.cli import cli as jira_cli


@click.group('cli')
@click.version_option(f'{APP_VERSION}', prog_name=APP_NAME)
@click.pass_context
def cli(ctx):
    """Bending Atlassian to its will since 2020!"""
    ctx.obj = {
        'config': config
    }


@cli.command('config', no_args_is_help=True)
@click.option('--edit', '-e', is_flag=True, default=False, help="edit config file")
@click.option('--create', '-c', is_flag=True, default=False, help="create config file")
@click.option('--delete', '-d', is_flag=True, default=False, help="delete config file")
@click.option('--path', '-p', is_flag=True, default=False, help="show path to config file")
@click.option('--local', '-l', is_flag=True, default=False, help="manage local config file")
def cli_config(edit, delete, create, path, local):
    """Manage bender config.

    --local manges config file within the local directory.

    \b
    Examples:
    bender config --path
    bender config --local --path
    bender config --create --edit
    bender config --local --create --edit
    """
    _config_file = config_file

    if local:
        _config_file = local_config_file

    if delete:
        os.unlink(_config_file)

    if create:
        with click.open_file(_config_file, 'w') as f:
            config.write(f)

    if edit:
        click.edit(filename=_config_file)

    if path:
        click.echo(click.format_filename('{}'.format(_config_file)))


cli.add_command(jira_cli)
cli.add_command(crowd_cli)
cli.add_command(confluence_cli)

import click

from bender.util.connect import AppConnect
from bender.util.writer import AppWriter
from bender import config, json_headers

confluence_config = config['confluence']


@click.group('confluence')
@click.option('--server', required=True, default=confluence_config.get('server'), help='connection server')
@click.option('--username', required=True, default=confluence_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=confluence_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=confluence_config.get('default_output'),
              type=click.Choice(AppWriter.FORMATS),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Confluence Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj.update({
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=confluence_config.get('cookie_store')),
        'writer': AppWriter(output=output, config_section='confluence'),
        'config': ctx.obj['config']['confluence'],
        'output': output
    })


@cli.command('status')
@click.pass_context
def cli_confluence_status(ctx):
    """Confluence application status (read only)."""
    confluence_status_path = "status"
    _res = ctx.obj['connect'].get(confluence_status_path, headers=json_headers)
    ctx.obj['writer'].out(_res)

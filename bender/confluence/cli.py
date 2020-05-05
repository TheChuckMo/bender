import click

from bender.utils import config, AppConnect, write_out, json_headers

confluence_config = config['confluence']


@click.group('confluence')
@click.option('--server', required=True, default=confluence_config.get('server'), help='connection server')
@click.option('--username', required=True, default=confluence_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=confluence_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=config['output'].get('default_output'),
              type=click.Choice(['yaml', 'json', 'raw']),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Confluence Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=confluence_config.get('cookie_store')),
        'output': output
    }


@cli.command('status')
@click.pass_context
def confluence_status(ctx):
    """Confluence application status (read only)."""
    confluence_status_path = "status"
    _res = ctx.obj['connect'].get(confluence_status_path, headers=json_headers)
    write_out(data=_res, output=ctx.obj['output'])

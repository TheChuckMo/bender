import click

from bender.utils import config, AppConnect, AppWriter, json_headers

crowd_config = config['crowd']


@click.group('crowd')
@click.option('--server', required=True, default=crowd_config.get('server'), help='connection server')
@click.option('--username', required=True, default=crowd_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=crowd_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=crowd_config.get('default_output'),
              type=click.Choice(AppWriter.FORMATS),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Crowd Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=crowd_config.get('cookie_store')),
        'writer': AppWriter(output=output, section='crowd')
    }


@cli.command('status')
@click.pass_context
def crowd_status(ctx):
    """Crowd application status (read only)."""
    crowd_status_path = 'status'
    _res = ctx.obj['connect'].get(crowd_status_path, headers=json_headers)
    ctx.obj['writer'].out(_res)

import click

from ..utils import config, AppConnect, write_out

crowd_config = config['crowd']

# headers
json_headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
form_headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Atlassian-Token': 'no-check'
}
no_check_headers = {
    'X-Atlassian-Token': 'no-check'
}

# API paths
crowd_status_path = "/status"


@click.group('crowd')
@click.option('--server', required=True, default=crowd_config.get('server'), help='connection server')
@click.option('--username', required=True, default=crowd_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=crowd_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=config['output'].get('default_output'),
              type=click.Choice(['yaml', 'json', 'raw']),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Crowd Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=crowd_config.get('cookie_store')),
        'output': output
    }


@cli.command('status')
@click.pass_context
def crowd_status(ctx):
    """Crowd application status (read only)."""
    _res = ctx.obj['connect'].get_json(crowd_status_path, headers=json_headers)
    write_out(data=_res, output=ctx.obj['output'])

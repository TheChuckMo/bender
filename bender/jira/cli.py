import json

import click

from bender.jira.cli_authconfig import jira_authconfig
from bender.jira.cli_cluster import jira_cluster
from bender.jira.cli_index import jira_index
from bender.jira.cli_property import jira_property
from bender.jira.cli_session import jira_session
from bender.jira.cli_webhook import jira_webhook
from bender.utils import config, AppConnect, write_out, json_headers

jira_config = config['jira']


@click.group('jira')
@click.option('--server', required=True, default=jira_config.get('server'), help='connection server')
@click.option('--username', required=True, default=jira_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=jira_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=config['output'].get('default_output'),
              type=click.Choice(['yaml', 'json', 'raw']),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Jira Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=jira_config.get('cookie_store')),
        'output': output
    }


cli.add_command(jira_index)
cli.add_command(jira_cluster)
cli.add_command(jira_property)
cli.add_command(jira_authconfig)
cli.add_command(jira_webhook)
cli.add_command(jira_session)


@cli.command('status')
@click.pass_context
def jira_status(ctx):
    """Jira application status (read only)."""
    jira_status_path = "status"
    _res = ctx.obj['connect'].get(jira_status_path, headers=json_headers, auth=False)
    write_out(data=_res, output=ctx.obj['output'])


@cli.command('configuration')
@click.pass_context
def jira_configuration(ctx):
    """Jira server configuration (read only)."""
    jira_configuration_path = "/rest/api/2/configuration"
    _res = ctx.obj['connect'].get(jira_configuration_path, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@cli.command('user', no_args_is_help=True)
@click.argument('name', default=None)
@click.option('--password', default=None, type=str, help="Set Jira user password.")
@click.pass_context
def jira_user(ctx, name, password):
    """Jira user password.

    name    Jira username.
    \b
    """
    jira_user_path = '/rest/api/2/user'
    if password:
        params = {
            'username': name
        }
        data = json.dumps({
            'password': password
        })
        _res = ctx.obj['connect'].put(f'{jira_user_path}/password', headers=json_headers, params=params, data=data,
                                      auth=True)
        write_out(data=_res, output=ctx.obj['output'])
    else:
        params = {
            'username': name
        }
        _res = ctx.obj['connect'].get(jira_user_path, headers=json_headers, params=params, auth=True)
        write_out(data=_res, output=ctx.obj['output'])


@cli.command('serverinfo', no_args_is_help=True)
@click.argument('action', type=click.Choice(['get', 'baseUrl']), default='get')
@click.option('--value', default=None, type=str, help="value to set.")
@click.option('--health-check', is_flag=True, default=False, help="run a health check")
@click.pass_context
def jira_serverinfo(ctx, action, value, health_check):
    """Jira server information.

    \b
    get         view serverinfo.
    baseUrl     set baseUrl to --value <url>.
    """
    jira_serverinfo_path = "rest/api/2/serverInfo"
    jira_settings_path = "rest/api/2/settings"
    if action is 'get':
        params = {
            'doHealthCheck': health_check
        }
        _res = ctx.obj['connect'].get(jira_serverinfo_path, params=params, headers=json_headers, auth=True)
        write_out(data=_res, output=ctx.obj['output'])

    if action is 'baseUrl':
        if not value:
            click.echo('--value required to set baseUrl')
            exit(1)

        _res = ctx.obj['connect'].put(f'{jira_settings_path}/baseUrl', data=value, auth=True)
        write_out(data=_res, output=ctx.obj['output'])

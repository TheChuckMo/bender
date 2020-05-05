import click

from bender.jira.cli_authconfig import jira_authconfig
from bender.jira.cli_cluster import jira_cluster
from bender.jira.cli_index import jira_index
from bender.jira.cli_property import jira_property
from bender.jira.cli_session import jira_session
from bender.jira.cli_webhook import jira_webhook
from bender.jira.cli_user import jira_user
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
    """Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=jira_config.get('cookie_store')),
        'output': output
    }


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


@cli.command('baseUrl')
@click.option('--value', '-v', default=None, type=str, required=True, help="baseUrl of server.")
@click.pass_context
def jira_baseurl(ctx, value):
    """Set Jira baseUrl."""
    jira_settings_path = "rest/api/2/settings"
    _res = ctx.obj['connect'].put(f'{jira_settings_path}/baseUrl', data=value, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@cli.command('serverinfo', no_args_is_help=True)
@click.option('--health-check', '-h', is_flag=True, default=False, help="run a health check")
@click.pass_context
def jira_serverinfo(ctx, health_check):
    """Jira server information and health-check."""
    jira_serverinfo_path = "rest/api/2/serverInfo"
    params = {
        'doHealthCheck': health_check
    }
    _res = ctx.obj['connect'].get(jira_serverinfo_path, params=params, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


cli.add_command(jira_index)
cli.add_command(jira_cluster)
cli.add_command(jira_property)
cli.add_command(jira_authconfig)
cli.add_command(jira_webhook)
cli.add_command(jira_session)
cli.add_command(jira_user)
import click

from bender.jira.cli_authconfig import cli_jira_authconfig
from bender.jira.cli_cluster import cli_jira_cluster
from bender.jira.cli_index import cli_jira_index
from bender.jira.cli_property import cli_jira_property
from bender.jira.cli_session import cli_jira_session
from bender.jira.cli_user import cli_jira_user
from bender.jira.cli_webhook import cli_jira_webhook
from bender.jira.cli_email import cli_jira_email
from bender.jira.cli_insight import cli_jira_insight
from bender.jira.cli_upm import cli_jira_upm
from bender.util.connect import AppConnect
from bender.util.writer import AppWriter
from bender import config, json_headers

jira_config = config['jira']


@click.group('jira')
@click.option('--server', required=True, default=jira_config.get('server'), help='connection server')
@click.option('--username', required=True, default=jira_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=jira_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=jira_config.get('default_output'),
              type=click.Choice(AppWriter.FORMATS),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Server administration.

    \b
    Examples:

    bender jira --username juser1 --password 'secret' --server http://localhost:8080 status
    """
    click.secho(f'server: {server}')
    if not password:
        password = click.prompt(f'{username} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj.update({
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=ctx.obj['config']['jira'].get('cookie_store')),
        'writer': AppWriter(output=output, config_section='jira'),
        'config': ctx.obj['config']['jira'],
        'output': output
    })


@cli.command('status')
@click.pass_context
def cli_jira_status(ctx):
    """Application Status (read only)."""
    jira_status_path = "status"
    _res = ctx.obj['connect'].get(jira_status_path, headers=json_headers, auth=False)
    ctx.obj['writer'].out(_res)


@cli.command('configuration')
@click.pass_context
def cli_jira_configuration(ctx):
    """Show server configuration (read only)."""
    jira_configuration_path = "/rest/api/2/configuration"
    _res = ctx.obj['connect'].get(jira_configuration_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli.command('baseUrl', no_args_is_help=True)
@click.argument('value', type=str, required=True)
@click.pass_context
def cli_jira_baseurl(ctx, value):
    """Set baseUrl.

    value       baseUrl to set

    \b
    Examples:
    bender jira baseUrl https://example.com/jira

    """
    jira_settings_path = "rest/api/2/settings"
    _res = ctx.obj['connect'].put(f'{jira_settings_path}/baseUrl', data=value, auth=True)
    ctx.obj['writer'].out(_res)


@cli.command('serverinfo')
@click.option('--health-check', '-h', is_flag=True, default=False, help="run a health check")
@click.pass_context
def cli_jira_serverinfo(ctx, health_check):
    """Server information and health-check.

    \b
    Examples:
    bender jira serverinfo
    bender jira serverinfo --health-check
    """
    jira_serverinfo_path = "rest/api/2/serverInfo"
    params = {
        'doHealthCheck': health_check
    }
    _res = ctx.obj['connect'].get(jira_serverinfo_path, params=params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


cli.add_command(cli_jira_index)
cli.add_command(cli_jira_email)
cli.add_command(cli_jira_cluster)
cli.add_command(cli_jira_property)
cli.add_command(cli_jira_authconfig)
cli.add_command(cli_jira_webhook)
cli.add_command(cli_jira_session)
cli.add_command(cli_jira_user)
cli.add_command(cli_jira_insight)
cli.add_command(cli_jira_upm)

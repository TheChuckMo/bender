import click
import requests
import json
from ..utils import config


# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"


@click.group('jira')
@click.option('--server', required=True, default=config.get('account', 'server', fallback=None),
              help='connection server')
@click.option('--username', required=True, default=config.get('account', 'username', fallback=None),
              help="connection username")
@click.option('--password', required=True, show_default=False, default=config.get('account', 'password', fallback=None),
              help='connection password')
@click.pass_context
def cli(ctx, server, username, password):
    """Manage Atlassian Jira Server"""
    print('# {}'.format(server))
    #print('username: {}'.format(username))
    ctx.obj = {
        'server': server,
        'auth': (username, password)
    }


@cli.command('status')
@click.pass_context
def jira_status(ctx):
    """Jira application status"""
    server = ctx.obj.get('server')
    url = '{server}{api}'.format(server=server, api=jira_status_path)
    #print('url: {}'.format(url))
    res = requests.get(url)
    #print('status: {}'.format(res.json()))
    print(json.dumps(res.json(), indent=2))


# @jira_cli.command('settings')
# @click.pass_context
# def jira_settings(ctx):
#     session = ctx.obj.get('session')
#     server = ctx.obj.get('server')
#     url = '{server}{api}'.format(server=server, api=jira_settings_path)
#     print('url: {}'.format(url))
#     res = session.get(url)
#     print('code: {}'.format(res.status_code))


@cli.command('info')
@click.pass_context
def jira_info(ctx):
    """Jira server information"""
    server = ctx.obj.get('server')
    url = '{server}{api}'.format(server=server, api=jira_serverinfo_path)
    res = requests.get(url)
    print(json.dumps(res.json(), indent=2))

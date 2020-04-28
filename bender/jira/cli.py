import click
import requests
import json
from ..utils import config


# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"
jira_cluster_nodes_path = "/rest/api/2/cluster/nodes"
jira_cluster_state_path = "/rest/api/2/cluster/zdu/state"


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
    res = requests.get(url)
    print(json.dumps(res.json(), indent=2))


# @cli.command('settings')
# @click.pass_context
# def jira_settings(ctx):
#     """Jira application settings"""
#     server = ctx.obj.get('server')
#     auth = ctx.obj.get('auth')
#     url = '{server}{api}'.format(server=server, api=jira_settings_path)
#     res = requests.get(url, auth=auth)
#     print('{}'.format(res.status_code))
#     print(json.dumps(res.json(), indent=2))


@cli.command('cluster')
@click.argument('item', type=click.Choice(['state', 'nodes']), default='state')
@click.pass_context
def jira_cluster(ctx, item):
    """Jira cluster nodes"""
    if item == 'state':
        api_path=jira_cluster_state_path
    else:
        api_path=jira_cluster_nodes_path

    server = ctx.obj.get('server')
    auth = ctx.obj.get('auth')
    url = '{server}{api}'.format(server=server, api=api_path)
    res = requests.get(url, auth=auth)
    print('{}'.format(res.status_code))
    print(json.dumps(res.json(), indent=2))


@cli.command('info')
@click.pass_context
def jira_info(ctx):
    """Jira server information"""
    server = ctx.obj.get('server')
    url = '{server}{api}'.format(server=server, api=jira_serverinfo_path)
    res = requests.get(url)
    print(json.dumps(res.json(), indent=2))

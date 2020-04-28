import click
import requests
import json
import yaml
from ..utils import config, AppConnect

# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"
jira_cluster_nodes_path = "/rest/api/2/cluster/nodes"
jira_cluster_state_path = "/rest/api/2/cluster/zdu/state"
jira_configuration_path = "/rest/api/2/configuration"


@click.group('jira')
@click.option('--server', required=True, default=config.get('account', 'server', fallback=None),
              help='connection server')
@click.option('--username', required=True, default=config.get('account', 'username', fallback=None),
              help="connection username")
@click.option('--password', required=True, show_default=False, default=config.get('account', 'password', fallback=None),
              help='connection password')
@click.option('--output', '-o', default='yaml', type=click.Choice(['yaml', 'json']), help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Manage Atlassian Jira Server"""
    print('# {}'.format(server))
    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password),
        'output': output
    }


@cli.command('status')
@click.pass_context
def jira_status(ctx):
    """Jira application status"""
    _res = ctx.obj['connect'].get_json(jira_status_path)

    if ctx.obj['output'] is 'json':
        print(json.dumps(_res))
    else:
        print(yaml.safe_dump(_res))


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
    if item is 'state':
        api_path = jira_cluster_state_path
    else:
        api_path = jira_cluster_nodes_path

    _res = ctx.obj['connect'].get_json(api_path)

    if ctx.obj['output'] is 'json':
        print(json.dumps(_res))
    else:
        print(yaml.safe_dump(_res))


@cli.command('configuration')
@click.pass_context
def jira_configuration(ctx):
    """Jira server information"""
    _res = ctx.obj['connect'].get_json(jira_configuration_path)

    if ctx.obj['output'] is 'json':
        print(json.dumps(_res))
    else:
        print(yaml.safe_dump(_res))


@cli.command('info')
@click.pass_context
def jira_info(ctx):
    """Jira server information"""
    server = ctx.obj.get('server')
    url = '{server}{api}'.format(server=server, api=jira_serverinfo_path)
    res = requests.get(url)
    print(json.dumps(res.json(), indent=2))

    _res = ctx.obj['connect'].get_json(jira_serverinfo_path)

    if ctx.obj['output'] is 'json':
        print(json.dumps(_res))
    else:
        print(yaml.safe_dump(_res))

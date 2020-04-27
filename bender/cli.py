import click
import requests
import os
import configparser
import json

# read configuration file
config = configparser.ConfigParser()
config_file = os.path.join(click.get_app_dir('bender'), 'config.ini')
config.read(config_file)
# print('config file: {}'.format(config_file))

# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"


@click.group('cli')
def cli():
    pass


@cli.command('config')
def cli_config():
    print('{}'.format(config_file))


@cli.group('jira')
@click.option('--server', required=True, default=config.get('account', 'server', fallback=None),
              help='connection server')
@click.option('--username', required=True, default=config.get('account', 'username', fallback=None),
              help="connection username")
@click.option('--password', required=True, show_default=False, default=config.get('account', 'password', fallback=None),
              help='connection password')
@click.pass_context
def jira_cli(ctx, server, username, password):
    print('# {}'.format(server))
    #print('username: {}'.format(username))
    ctx.obj = {
        'server': server,
        'auth': (username, password)
    }


@jira_cli.command('status')
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


@jira_cli.command('info')
@click.pass_context
def jira_info(ctx):
    """Jira server information"""
    server = ctx.obj.get('server')
    url = '{server}{api}'.format(server=server, api=jira_serverinfo_path)
    res = requests.get(url)
    print(json.dumps(res.json(), indent=2))


def connect(username, password):
    req = requests.session()
    req.headers.update({'Content-Type': 'application/json'})
    # req.auth = (username, password)
    return req

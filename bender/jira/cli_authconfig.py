import click

from bender.utils import json_headers
import json


@click.group('authconfig')
@click.pass_context
def jira_authconfig(ctx):
    """Jira authentication configuration."""
    pass


@jira_authconfig.command('get')
@click.pass_context
def jira_authconfig_get(ctx):
    """get authentication config."""
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    _res = ctx.obj['connect'].get(jira_authconfig_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@jira_authconfig.command('set')
@click.option('--value', '-v', default=None, required=True, type=str, help="value to set")
@click.option('--key', '-k', default=None, required=True, type=str, help="key to set")
@click.pass_context
def jira_authconfig_set(ctx, key, value):
    """set authentication config."""
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    data = json.dumps({
        key: value
    })
    _res = ctx.obj['connect'].put(jira_authconfig_path, headers=json_headers, data=data, auth=True)
    ctx.obj['writer'].out(_res)


@jira_authconfig.command('load')
@click.argument('file', type=click.File('r'))
@click.pass_context
def jira_authconfig_load(ctx, file):
    """set authentication config."""
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    data = json.dumps(json.load(file))
    #click.echo(data)
    _res = ctx.obj['connect'].put(jira_authconfig_path, headers=json_headers, data=data, auth=True)
    ctx.obj['writer'].out(_res)

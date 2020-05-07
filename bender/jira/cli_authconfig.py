import click

from bender.utils import json_headers


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
@click.option('--value', default=None, required=True, type=str, help="json value for authconfig")
@click.pass_context
def jira_authconfig_set(ctx, action, value):
    """set authentication config."""
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    click.echo('not yet implemented.')

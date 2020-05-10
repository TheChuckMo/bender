import json

import click

from bender.utils import json_headers


@click.group('authconfig')
@click.pass_context
def cli_jira_authconfig(ctx):
    """Jira authentication configuration.

    \b
    Examples:
    bender jira authconfig get
    bender jira authconfig set allow-saml-redirect-override false
    bender jira authconfig load authconfig.json
    """
    pass


@cli_jira_authconfig.command('get')
@click.pass_context
def cli_jira_authconfig_get(ctx):
    """get authentication config.

    \b
    Examples:
    bender jira authconfig get
    """
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    _res = ctx.obj['connect'].get(jira_authconfig_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_authconfig.command('set')
@click.argument('key', required=True, type=str)
@click.argument('value', required=True, type=str)
@click.pass_context
def cli_jira_authconfig_set(ctx, key, value):
    """Set authentication parameter.

    key     parameter to set.
    value   value to set.

    \b
    Examples:
    bender jira authconfig set allow-saml-redirect-override false
    """
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    data = json.dumps({
        key: value
    })
    _res = ctx.obj['connect'].put(jira_authconfig_path, headers=json_headers, data=data, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_authconfig.command('load')
@click.argument('file', type=click.File('r'))
@click.pass_context
def cli_jira_authconfig_load(ctx, file):
    """Load authentication config from file.

    \b
    Examples:
    bender jira authconfig load authconfig.json
    """
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    data = json.dumps(json.load(file))
    # click.echo(data)
    _res = ctx.obj['connect'].put(jira_authconfig_path, headers=json_headers, data=data, auth=True)
    ctx.obj['writer'].out(_res)

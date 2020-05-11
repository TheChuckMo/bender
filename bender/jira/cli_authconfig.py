import json

import click

from bender import json_headers


@click.group('authconfig')
@click.pass_context
def cli_jira_authconfig(ctx):
    """Authentication configuration.

    \b
    Examples:
    bender jira authconfig get
    bender jira authconfig set allow-saml-redirect-override false
    bender jira authconfig import authconfig.json
    bender jira authconfig export authconfig.json
    """
    pass


@cli_jira_authconfig.command('get')
@click.pass_context
def cli_jira_authconfig_get(ctx):
    """Get authconfig.

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
    """Set authconfig parameter.

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


@cli_jira_authconfig.command('import')
@click.argument('file', type=click.File('r'))
@click.pass_context
def cli_jira_authconfig_import(ctx, file):
    """Import authconfig from file.

    \b
    Examples:
    bender jira authconfig import authconfig.json
    """
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    data = json.dumps(json.load(file))
    _res = ctx.obj['connect'].put(jira_authconfig_path, headers=json_headers, data=data, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_authconfig.command('export')
@click.argument('file', type=click.File('w'))
@click.pass_context
def cli_jira_authconfig_export(ctx, file):
    """Export authconfig to file.

    \b
    Examples:
    bender jira authconfig export authconfig.json
    """
    jira_authconfig_path = "rest/authconfig/1.0/saml"
    _res = ctx.obj['connect'].get(jira_authconfig_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res, output='json', file=file)

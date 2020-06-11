import click

from bender import json_headers, no_check_headers, form_headers


@click.group('plugins')
@click.pass_context
def cli_jira_plugins(ctx):
    """Universal Plugin Manager."""
    pass


@cli_jira_plugins.command('settings')
@click.pass_context
def cli_jira_plugin_settings(ctx):
    """UPM settings."""
    jira_plugin_settings_path = 'rest/plugins/1.0/settings'
    _res = ctx.obj['connect'].get(jira_plugin_settings_path, headers=no_check_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_plugins.command('installed')
@click.option('--updates', '-u', default=False, is_flag=True, help="Plugins requiring an update.")
@click.pass_context
def cli_jira_plugin_installed(ctx, updates):
    """UPM settings."""
    _params = {'updates': updates}
    jira_plugin_installed_path = 'rest/plugins/1.0/'
    _res = ctx.obj['connect'].get(jira_plugin_installed_path, params=_params, headers=no_check_headers, auth=True)
    ctx.obj['writer'].out(_res)
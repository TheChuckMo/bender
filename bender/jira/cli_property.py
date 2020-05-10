import json

import click

from bender.utils import json_headers


@click.group('property')
@click.pass_context
def cli_jira_property(ctx):
    """Jira application-properties.

    \b
    Examples:
    bender jira property list
    bender jira property list --advanced
    bender jira property list --key 'jira.*'
    bender jira property get cluster.task.cleanup.offline.node.threshold
    bender jira property get 'jira.search.*'
    bender jira property set jira.quicksearch.max.concurrent.searches 22
    bender jira property set jira.lf.top.bgcolour '#ED6D23'
    """
    pass


@cli_jira_property.command('list')
@click.option('--advanced', '-a', is_flag=True, default=False, help="list advanced application-properties.")
@click.option('--key', '-k', default=None, type=str, help="key (id) filter.")
@click.pass_context
def cli_jira_property_list(ctx, advanced, key):
    """list application-properties (--advanced).

    \b
    Examples:
    bender jira property list
    bender jira property list --advanced
    bender jira property list --key 'jira.*'
    """
    jira_application_properties_path = "rest/api/2/application-properties"
    jira_application_properties_advanced_path = "rest/api/2/application-properties/advanced-settings"
    _url = None
    params = None

    if key:
        params = {
            'keyFilter': key
        }

    if advanced:
        _url = jira_application_properties_advanced_path
    else:
        _url = jira_application_properties_path

    _res = ctx.obj['connect'].get(_url, params=params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_property.command('get')
@click.argument('key', type=str, required=True)
@click.pass_context
def cli_jira_property_get(ctx, key):
    """get application-property.

    \b
    Examples:
    bender jira property get cluster.task.cleanup.offline.node.threshold
    bender jira property get 'jira.search.*'

    """
    jira_application_properties_path = "rest/api/2/application-properties"
    params = None
    if key:
        params = {
            'keyFilter': key
        }

    _res = ctx.obj['connect'].get(jira_application_properties_path, params=params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_property.command('set')
@click.argument('key', type=str, required=True)
@click.argument('value', type=str, required=True)
@click.pass_context
def cli_jira_property_set(ctx, key, value):
    """set an application-property.

    key     property key to update.
    value   value for property.

    \b
    Examples:
    bender jira property set jira.quicksearch.max.concurrent.searches 22
    bender jira property set jira.lf.top.bgcolour '#ED6D23'
    """
    jira_application_properties_path = "rest/api/2/application-properties"
    data = json.dumps({
        "id": key,
        "value": value
    })
    _res = ctx.obj['connect'].put(f'{jira_application_properties_path}/{key}', data=data, headers=json_headers,
                                  auth=True)
    ctx.obj['writer'].out(_res)

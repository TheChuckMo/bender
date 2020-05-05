import json

import click

from bender.utils import json_headers, write_out


@click.group('property')
@click.pass_context
def jira_property(ctx):
    """Jira application-properties."""
    pass


@jira_property.command('list')
@click.option('--advanced', '-a', is_flag=True, default=False, help="list advanced application-properties.")
@click.option('--key', '-k', default=None, type=str, help="key (id) filter.")
@click.pass_context
def jira_property_list(ctx, advanced, key):
    """list application-properties (--advanced)."""
    jira_application_properties_path = "/rest/api/2/application-properties"
    jira_application_properties_advanced_path = "/rest/api/2/application-properties/advanced-settings"
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
    write_out(data=_res, output=ctx.obj['output'])


@jira_property.command('get')
@click.option('--key', '-k', default=None, type=str, required=True, help="property key (id) filter.")
@click.pass_context
def jira_property_get(ctx, key):
    """get application-property.

    \b
    $ bender jira property get --key cluster.task.cleanup.offline.node.threshold

    $ bender jira property get --key 'jira.search.*'

    """
    jira_application_properties_path = "/rest/api/2/application-properties"
    params = None
    if key:
        params = {
            'keyFilter': key
        }

    _res = ctx.obj['connect'].get(jira_application_properties_path, params=params, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@jira_property.command('set')
@click.option('--key', '-k', default=None, type=str, required=True, help="application-property key (id).")
@click.option('--value', '-v', default=None, type=str, required=True, help="application-property value.")
@click.pass_context
def jira_property_set(ctx, key, value):
    """set an application-property."""
    jira_application_properties_path = "/rest/api/2/application-properties"
    data = json.dumps({
        "id": key,
        "value": value
    })
    _res = ctx.obj['connect'].put(f'{jira_application_properties_path}/{key}', data=data, headers=json_headers,
                                  auth=True)
    write_out(data=_res, output=ctx.obj['output'])

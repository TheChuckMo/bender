import click

from ..utils import config, AppConnect, write_out

# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"
jira_cluster_nodes_path = "/rest/api/2/cluster/nodes"
jira_cluster_state_path = "/rest/api/2/cluster/zdu/state"
jira_configuration_path = "/rest/api/2/configuration"
jira_application_properties_advanced_path = "/rest/api/2/application-properties/advanced-settings"
jira_index_path = "/rest/api/2/index/summary"
jira_reindex_path = "/rest/api/2/reindex"


@click.group('jira')
@click.option('--server', required=True, default=config['account'].get('server'), help='connection server')
@click.option('--username', required=True, default=config['account'].get('username', fallback=None),
              help="connection username")
@click.option('--password', required=True, show_default=False, default=config['account'].get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=config['output'].get('default_output'), type=click.Choice(['yaml', 'json']),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Jira Server administration."""
    print('# {}'.format(server))
    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password),
        'output': output
    }


@cli.command('properties')
@click.argument('action', type=click.Choice(['view', 'set', 'get']), default='view')
@click.option('--advanced', '--ad', default=False, help="view advanced application-properties.")
@click.option('--id', 'propid', default=None, type=str, help="application-property id for get and set.")
@click.option('--value', default=None, type=str, help="application-property value for set.")
@click.pass_context
def jira_properties(ctx, action, advanced, propid, value):
    """Jira application-properties.

    \b
    view    (default) view application properties.
    set     set a property with --id and --value.
    get     get a property with --id.
    """
    if action is 'view':
        if advanced:
            _res = ctx.obj['connect'].get_json(jira_application_properties_advanced_path)
        else:
            _res = ctx.obj['connect'].get_json(jira_application_properties_path)

    if action is 'get':
        if not propid:
            click.secho('--id <application-property id> required.', fg='red', blink=True, bold=True, err=True)
            exit(1)
        _res = ctx.obj['connect'].get_json(f'{jira_application_properties_path}/{propid}')

    write_out(data=_res, output=ctx.obj['output'])


@cli.command('index')
@click.argument('action', type=click.Choice(['summary', 'reindex', 'status']), default='summary')
@click.option('--comments/--no-comments', default=True, help="reindex comments")
@click.option('--history/--no-history', default=True, help="reindex change history")
@click.option('--worklogs/--no-worklogs', default=True, help="reindex work logs")
@click.option('--taskid', default=None, help="reindex task id")
@click.pass_context
def jira_index(ctx, action, comments, history, worklogs, taskid):
    """Jira index.

    \b
    summary     (default) show index summary
    reindex     start a reindex
    status      status of reindex, opt: --taskid
    """
    if action is 'reindex':
        params = {
            'indexComments': comments,
            'indexChangeHistory': history,
            'indexWorklogs': worklogs,
            'type': 'BACKGROUND_PREFERRED'
        }
        _res = ctx.obj['connect'].post(jira_reindex_path, params=params)
    elif action is 'status' and taskid is not None:
        params = {
            'taskId': taskid
        }
        _res = ctx.obj['connect'].get_json(jira_reindex_path, params=params)
    elif action is 'status':
        _res = ctx.obj['connect'].get_json(jira_reindex_path)
    else:
        _res = ctx.obj['connect'].get_json(jira_index_path)

    write_out(data=_res, output=ctx.obj['output'])


@cli.command('status')
@click.pass_context
def jira_status(ctx):
    """Jira application status."""
    _res = ctx.obj['connect'].get_json(jira_status_path)

    write_out(data=_res, output=ctx.obj['output'])


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
    """Jira cluster.

    \b
    state   (default) cluster state
    nodes   cluster nodes state
    """
    if item is 'state':
        api_path = jira_cluster_state_path
    else:
        api_path = jira_cluster_nodes_path

    _res = ctx.obj['connect'].get_json(api_path)

    write_out(data=_res, output=ctx.obj['output'])


@cli.command('configuration')
@click.pass_context
def jira_configuration(ctx):
    """Jira server configuration."""
    _res = ctx.obj['connect'].get_json(jira_configuration_path)

    write_out(data=_res, output=ctx.obj['output'])


@cli.command('serverinfo')
@click.pass_context
def jira_serverinfo(ctx):
    """Jira server information."""
    _res = ctx.obj['connect'].get_json(jira_serverinfo_path)

    write_out(data=_res, output=ctx.obj['output'])

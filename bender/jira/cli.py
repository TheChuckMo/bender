import json
import os

import click

from ..utils import config, AppConnect, write_out, json_headers, no_check_headers

jira_config = config['jira']


# json_headers = {
#     'Content-Type': 'application/json',
#     'Accept': 'application/json'
# }
# form_headers = {
#     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
# }
# no_check_headers = {
#     'X-Atlassian-Token': 'no-check'
# }


@click.group('jira')
@click.option('--server', required=True, default=jira_config.get('server'), help='connection server')
@click.option('--username', required=True, default=jira_config.get('username', fallback=None),
              help="connection username")
@click.option('--password', show_default=False, default=jira_config.get('password', fallback=None),
              help='connection password')
@click.option('--output', '--out', default=config['output'].get('default_output'),
              type=click.Choice(['yaml', 'json', 'raw']),
              help="output format")
@click.pass_context
def cli(ctx, server, username, password, output):
    """Jira Server administration."""
    if not password:
        password = click.prompt(f'{server} password', hide_input=True, confirmation_prompt=True, show_default=False)

    ctx.obj = {
        'connect': AppConnect(server, username=username, password=password,
                              cookie_store=jira_config.get('cookie_store')),
        'output': output
    }


@cli.command('status')
@click.pass_context
def jira_status(ctx):
    """Jira application status (read only)."""
    jira_status_path = "/status"
    _res = ctx.obj['connect'].get(jira_status_path, headers=json_headers, auth=False)
    write_out(data=_res, output=ctx.obj['output'])


@cli.command('session', no_args_is_help=True)
@click.option('--delete', is_flag=True, default=False, help="Delete session cookies.")
@click.option('--cookies', is_flag=True, default=False, help="List cookies in store.")
@click.option('--view', is_flag=True, default=False, help="View Jira session.")
@click.option('--login', is_flag=True, default=False, help="login to Jira session.")
@click.option('--logout', is_flag=True, default=False, help="logout of Jira session and delete cookies.")
@click.option('--websudo', is_flag=True, default=False, help="Grant websudo access.")
@click.option('--release', is_flag=True, default=False, help="Release websudo access.")
@click.pass_context
def jira_session(ctx, delete, cookies, view, login, logout, websudo, release):
    """Jira session."""
    jira_session_path = "/rest/auth/1/session"
    jira_websudo_jspa_path = "/secure/admin/WebSudoAuthenticate.jspa"
    jira_websudo_path = "/rest/auth/1/websudo"
    if release:
        _res = ctx.obj['connect'].delete(jira_websudo_path, headers=no_check_headers)
        write_out(_res, ctx.obj['output'])

    if logout:
        _res = ctx.obj['connect'].delete(jira_session_path, headers=json_headers)
        write_out(_res, ctx.obj['output'])
        delete = True

    if delete:
        if os.unlink(jira_config.get('cookie_store')):
            click.secho('cookie store deleted.', fg='blue')

    if login:
        data = json.dumps({
            'username': str(ctx.obj['connect'].username),
            'password': str(ctx.obj['connect'].password)
        })

        _res = ctx.obj['connect'].post(jira_session_path, headers=json_headers, data=data)

        write_out(_res, ctx.obj['output'])

    if websudo:
        websudo_token: bool = False
        data = {
            'webSudoPassword': ctx.obj['connect'].password,
            'webSudoIsPost': "False"
        }
        ans = ctx.obj['connect'].post(jira_websudo_jspa_path, headers=json_headers.update(no_check_headers), data=data,
                                      auth=True)
        if ans:
            # taken directly from atlassian python api
            atl_token = \
            ans.get('reason').split('<meta id="atlassian-token" name="atlassian-token" content="')[1].split('\n')[
                0].split('"')[0]
        if atl_token:
            ctx.obj['connect'].update_cookies({'atl_token': atl_token})
            websudo_token = True
        write_out(websudo_token, ctx.obj['output'])

    if view:
        _res = ctx.obj['connect'].get(jira_session_path, headers=json_headers)
        write_out(_res, ctx.obj['output'])

    if cookies:
        for cookie in ctx.obj['connect'].session.cookies:
            click.echo(cookie)


@cli.command('property', no_args_is_help=True)
@click.argument('action', type=click.Choice(['view', 'set', 'get']), default='view')
@click.option('--advanced', '--ad', is_flag=True, default=False, help="view advanced application-properties.")
@click.option('--id', 'propid', default=None, type=str, help="application-properties id for get and set.")
@click.option('--value', default=None, type=str, help="application-properties value for set.")
@click.pass_context
def jira_property(ctx, action, advanced, propid, value):
    """Jira application-properties.

    \b
    view    view application properties, --advanced for more.
    set     set a property with --id and --value.
    get     get a property with --id.
    """
    jira_application_properties_path = "/rest/api/2/application-properties"
    jira_application_properties_advanced_path = "/rest/api/2/application-properties/advanced-settings"
    if action is 'view':
        if advanced:
            _res = ctx.obj['connect'].get(jira_application_properties_advanced_path, headers=json_headers, auth=True)
        else:
            _res = ctx.obj['connect'].get(jira_application_properties_path, headers=json_headers, auth=True)

    if action is 'get':
        if not propid:
            click.secho('--id <application-property id> required.', fg='red', blink=True, bold=True, err=True)
            exit(1)
        params = {
            'keyFilter': propid
        }
        _res = ctx.obj['connect'].get(jira_application_properties_path, params=params, headers=json_headers, auth=True)

    if action is 'set':
        if not propid:
            click.secho('--id <application-property id> required.', fg='red', blink=True, bold=True, err=True)
            exit(1)
        if not value:
            click.secho('--value <application-property value> required.', fg='red', blink=True, bold=True, err=True)
            exit(1)

        data = json.dumps({
            "id": propid,
            "value": value
        })
        _res = ctx.obj['connect'].put(f'{jira_application_properties_path}/{propid}', data=data, headers=json_headers,
                                      auth=True)

    write_out(data=_res, output=ctx.obj['output'])


@cli.command('index', no_args_is_help=True)
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
    jira_index_path = "/rest/api/2/index/summary"
    jira_reindex_path = "/rest/api/2/reindex"
    if action is 'reindex':
        params = {
            'indexComments': comments,
            'indexChangeHistory': history,
            'indexWorklogs': worklogs,
            'type': 'BACKGROUND_PREFERRED'
        }
        _res = ctx.obj['connect'].post(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                       allow_redirects=False)

    if action is 'status' and taskid is not None:
        params = {
            'taskId': taskid
        }
        _res = ctx.obj['connect'].get(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                      allow_redirects=False)
    elif action is 'status':
        _res = ctx.obj['connect'].get(jira_reindex_path, headers=json_headers, auth=True, allow_redirects=False)

    if action is 'summary':
        _res = ctx.obj['connect'].get(jira_index_path, headers=json_headers, auth=True)

    write_out(data=_res, output=ctx.obj['output'])


# @cli.command('settings')
# @click.pass_context
# def jira_settings(ctx):
#     """Jira application settings"""
# jira_settings_path = "/rest/api/2/settings"
#     server = ctx.obj.get('server')
#     auth = ctx.obj.get('auth')
#     url = '{server}{api}'.format(server=server, api=jira_settings_path)
#     res = requests.get(url, auth=auth)
#     print('{}'.format(res.status_code))
#     print(json.dumps(res.json(), indent=2))


@cli.command('cluster', no_args_is_help=True)
@click.argument('action', type=click.Choice(['state', 'nodes']), default='state')
@click.pass_context
def jira_cluster(ctx, action):
    """Jira cluster.

    \b
    state   (default) cluster state
    nodes   cluster nodes state
    """
    jira_cluster_nodes_path = "/rest/api/2/cluster/nodes"
    jira_cluster_state_path = "/rest/api/2/cluster/zdu/state"
    if action is 'state':
        _res = ctx.obj['connect'].get(jira_cluster_state_path, headers=json_headers, auth=True)
        write_out(data=_res, output=ctx.obj['output'])

    if action is 'nodes':
        _res = ctx.obj['connect'].get(jira_cluster_nodes_path, headers=json_headers, auth=True)
        write_out(data=_res, output=ctx.obj['output'])


@cli.command('configuration')
@click.pass_context
def jira_configuration(ctx):
    """Jira server configuration (read only)."""
    jira_configuration_path = "/rest/api/2/configuration"
    _res = ctx.obj['connect'].get(jira_configuration_path, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@cli.command('serverinfo')
@click.pass_context
def jira_serverinfo(ctx):
    """Jira server information (read only)."""
    jira_serverinfo_path = "/rest/api/2/serverInfo"
    _res = ctx.obj['connect'].get(jira_serverinfo_path, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])

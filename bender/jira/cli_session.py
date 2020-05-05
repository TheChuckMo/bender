import json
import os

import click

from bender.utils import no_check_headers, write_out, json_headers


@click.command('session', no_args_is_help=True)
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
    jira_session_path = "rest/auth/1/session"
    jira_websudo_jspa_path = "secure/admin/WebSudoAuthenticate.jspa"
    jira_websudo_path = "rest/auth/1/websudo"
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

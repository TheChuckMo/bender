import json
import os

import click

from bender.utils import config
from bender.utils import no_check_headers, json_headers

jira_config = config['jira']


@click.group('session')
@click.pass_context
def cli_jira_session(ctx):
    """Jira session management.

    \b
    Examples:
    bender jira session get
    bender jira session logout
    bender jira session login
    bender jira session cookies --delete
    """
    pass


@cli_jira_session.command('login')
@click.pass_context
def cli_jira_session_login(ctx):
    """session login.

    \b
    Examples:
    bender jira session login
    """
    jira_session_path = "rest/auth/1/session"

    data = json.dumps({
        'username': str(ctx.obj['connect'].username),
        'password': str(ctx.obj['connect'].password)
    })

    _res = ctx.obj['connect'].post(jira_session_path, headers=json_headers, data=data)
    ctx.obj['writer'].out(_res)


@cli_jira_session.command('logout')
@click.pass_context
def cli_jira_session_logout(ctx):
    """Session logout.

    \b
    Examples:
    bender jira session logout
    """
    jira_session_path = "rest/auth/1/session"
    _res = ctx.obj['connect'].delete(jira_session_path, headers=json_headers)
    ctx.obj['writer'].out(_res)


@cli_jira_session.command('get')
@click.pass_context
def cli_jira_session_get(ctx):
    """Session get.

    \b
    Examples:
    bender jira session get
    bender jira session cookies --delete
    """
    jira_session_path = "rest/auth/1/session"
    _res = ctx.obj['connect'].get(jira_session_path, headers=json_headers)
    ctx.obj['writer'].out(_res)


@cli_jira_session.command('cookies')
@click.option('--delete', '-d', is_flag=True, default=False, help="Delete session cookies.")
@click.pass_context
def cli_jira_session_cookies(ctx, delete):
    """Session cookies.

    \b
    Examples:
    bender jira session cookies --delete
    """
    if delete:
        if os.unlink(jira_config.get('cookie_store')):
            click.secho('cookie store deleted.', fg='blue')

    for cookie in ctx.obj['connect'].session.cookies:
        click.echo(cookie)


@cli_jira_session.command('websudo')
@click.option('--release', is_flag=True, default=False, help="Release websudo access.")
@click.pass_context
def cli_jira_session_websudo(ctx, release):
    """Websudo."""
    jira_websudo_jspa_path = "secure/admin/WebSudoAuthenticate.jspa"
    jira_websudo_path = "rest/auth/1/websudo"

    if release:
        _res = ctx.obj['connect'].delete(jira_websudo_path, headers=no_check_headers)
        ctx.obj['writer'].out(_res)
        exit()

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

        ctx.obj['writer'].out([atl_token, websudo_token])

import json

import click

from bender.utils import json_headers


@click.group('user')
@click.argument('name', default=None, type=str, required=True)
@click.pass_context
def cli_jira_user(ctx, name):
    """Jira user.

    name    Jira user name.

    \b
    Examples:
    bender jira user juser1 get
    bender jira user juser1 password 'new-password'
    """
    ctx.obj.update({'username': name})


@cli_jira_user.command('get')
@click.pass_context
def cli_jira_user_get(ctx):
    """Get user information."""
    jira_user_path = 'rest/api/2/user'
    params = {
        'username': ctx.obj.get('username')
    }
    _res = ctx.obj['connect'].get(jira_user_path, headers=json_headers, params=params, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_user.command('password')
@click.argument('password', default=None, type=str)
@click.pass_context
def cli_jira_user_password(ctx, password):
    """Set user password.

    password    New password.
    \b
    """
    jira_user_path = 'rest/api/2/user'
    params = {
        'username': ctx.obj.get('username')
    }
    data = json.dumps({
        'password': password
    })
    _res = ctx.obj['connect'].put(f'{jira_user_path}/password', headers=json_headers, params=params, data=data,
                                  auth=True)
    ctx.obj['writer'].out(_res)

import json

import click

from bender.utils import json_headers, write_out


@click.group('user')
@click.pass_context
def jira_user(ctx):
    """Jira user."""
    pass


@jira_user.command('get', no_args_is_help=True)
@click.argument('name', default=None)
@click.pass_context
def jira_user_get(ctx, name):
    """Get user."""
    jira_user_path = '/rest/api/2/user'
    params = {
        'username': name
    }
    _res = ctx.obj['connect'].get(jira_user_path, headers=json_headers, params=params, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@jira_user.command('user', no_args_is_help=True)
@click.argument('name', default=None)
@click.option('--password', default=None, required=True, type=str, help="New user password.")
@click.pass_context
def jira_user_password(ctx, name, password):
    """Set user password.

    name    Jira username.
    \b
    """
    jira_user_path = '/rest/api/2/user'
    params = {
        'username': name
    }
    data = json.dumps({
        'password': password
    })
    _res = ctx.obj['connect'].put(f'{jira_user_path}/password', headers=json_headers, params=params, data=data,
                                  auth=True)
    write_out(data=_res, output=ctx.obj['output'])

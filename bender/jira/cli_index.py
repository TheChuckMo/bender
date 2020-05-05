import click

from bender.utils import json_headers, write_out


@click.group('index')
@click.pass_context
def jira_index(ctx):
    """Jira index."""
    pass


@jira_index.command('state')
@click.pass_context
def jira_index_state(ctx):
    """Jira index state."""
    jira_index_path = "/rest/api/2/index/summary"
    _res = ctx.obj['connect'].get(jira_index_path, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@jira_index.command('reindex')
@click.option('--comments/--no-comments', default=True, help="reindex comments")
@click.option('--history/--no-history', default=True, help="reindex change history")
@click.option('--worklogs/--no-worklogs', default=True, help="reindex work logs")
@click.pass_context
def jira_index_reindex(ctx, comments, history, worklogs):
    """Jira run reindex."""
    jira_reindex_path = "/rest/api/2/reindex"
    _res = None
    params = {
        'indexComments': comments,
        'indexChangeHistory': history,
        'indexWorklogs': worklogs,
        'type': 'BACKGROUND_PREFERRED'
    }
    _res = ctx.obj['connect'].post(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                   allow_redirects=False)

    write_out(data=_res, output=ctx.obj['output'])


@jira_index.command('status')
@click.option('--id', 'task_id', default=None, help="reindex task id")
@click.pass_context
def jira_index_status(ctx, task_id):
    """Jira reindex status."""
    jira_reindex_path = "/rest/api/2/reindex"
    params = None
    _res = None
    if task_id is not None:
        params = {
            'taskId': task_id
        }

    _res = ctx.obj['connect'].get(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                  allow_redirects=False)
    write_out(data=_res, output=ctx.obj['output'])

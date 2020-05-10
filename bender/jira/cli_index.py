import click

from bender.utils import json_headers


@click.group('index')
@click.pass_context
def cli_jira_index(ctx):
    """Jira index.

    \b
    Examples:
    bender jira index state
    bender jira index reindex --no-comments
    bender jira index status
    bender jira index status --id 1110
    """
    pass


@cli_jira_index.command('state')
@click.pass_context
def cli_jira_index_state(ctx):
    """Jira index state.

    \b
    Examples:
    bender jira index state
    """
    jira_index_path = "rest/api/2/index/summary"
    _res = ctx.obj['connect'].get(jira_index_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_index.command('reindex')
@click.option('--comments/--no-comments', default=True, help="reindex comments")
@click.option('--history/--no-history', default=True, help="reindex change history")
@click.option('--worklogs/--no-worklogs', default=True, help="reindex work logs")
@click.pass_context
def cli_jira_index_reindex(ctx, comments, history, worklogs):
    """Jira run reindex.

    \b
    Examples:
    bender jira index reindex
    bender jira index reindex --comments --history --worklogs
    """
    jira_reindex_path = "rest/api/2/reindex"
    _res = None
    params = {
        'indexComments': comments,
        'indexChangeHistory': history,
        'indexWorklogs': worklogs,
        'type': 'BACKGROUND_PREFERRED'
    }
    _res = ctx.obj['connect'].post(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                   allow_redirects=False)

    ctx.obj['writer'].out(_res)


@cli_jira_index.command('status')
@click.option('--id', 'task_id', default=None, help="reindex task id")
@click.pass_context
def cli_jira_index_status(ctx, task_id):
    """Jira reindex status.

    Status of last reindex or by task id.

    Examples:
    bender jira index status
    bender jira index status --id 3932
    """
    jira_reindex_path = "rest/api/2/reindex"
    params = None
    _res = None
    if task_id is not None:
        params = {
            'taskId': task_id
        }

    _res = ctx.obj['connect'].get(jira_reindex_path, params=params, headers=json_headers, auth=True,
                                  allow_redirects=False)
    ctx.obj['writer'].out(_res)


@cli_jira_index.group('analyzer')
@click.pass_context
def cli_jira_index_analyzer(ctx):
    """Jira index analyzer.

    \b
    Examples:
    bender jira index analyzer state
    bender jira index analyzer statistics
    """
    pass


@cli_jira_index_analyzer.command('state')
@click.pass_context
def cli_jira_index_analyzer_state(ctx):
    """Jira index analyzer state.

    \b
    Examples:
    bender jira index analyzer state
    """
    jira_index_analyzer_state_path = "rest/indexanalyzer/1/state"
    _res = ctx.obj['connect'].get(jira_index_analyzer_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_index_analyzer.command('statistics')
@click.pass_context
def cli_jira_index_analyzer_state(ctx):
    """Jira index analyzer state.

    \b
    Examples:
    bender jira index analyzer statistics
    """
    jira_index_analyzer_statistics_path = "rest/indexanalyzer/1/statistics"
    _res = ctx.obj['connect'].get(jira_index_analyzer_statistics_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)
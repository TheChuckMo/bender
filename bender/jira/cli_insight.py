import click

from bender.utils import json_headers


@click.group('insight')
@click.pass_context
def cli_jira_insight(ctx):
    """Insight plugin.

    \b
    Examples:
    bender jira insight index path
    bender jira insight index persist
    bender jira insight index reindex start
    bender jira insight index reindex start --clean
    bender jira insight index reindex current-node
    bender jira insight index reindex current-node --clean
    bender jira insight index reindex object --id 220
    """
    pass


@cli_jira_insight.group('index')
@click.pass_context
def cli_jira_insight_index(ctx):
    """Insight index."""
    pass


@cli_jira_insight_index.command('path')
@click.pass_context
def cli_jira_insight_index_path(ctx):
    """Insight index path.

    Show Insight index path.

    \b
    Examples:
    bender jira insight index path
    """
    jira_insight_index_path = 'rest/insight/1.0/index/path'
    _res = ctx.obj['connect'].get(jira_insight_index_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_insight_index.command('persist')
@click.pass_context
def cli_jira_insight_index_persist(ctx):
    """Insight index persis.

    Persist Insight index to disk.

    \b
    Examples:
    bender jira insight index persist
    """
    jira_insight_index_persist_path = 'rest/insight/1.0/index/persist'
    _res = ctx.obj['connect'].post(jira_insight_index_persist_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_insight_index.group('reindex')
@click.pass_context
def cli_jira_insight_index_reindex(ctx):
    """Insight reindex."""
    pass


@cli_jira_insight_index_reindex.command('start')
@click.option('--clean/--no-clean', '-c', 'clean', default=False, is_flag=True, help='Clean before reindex.')
@click.pass_context
def cli_jira_insight_index_reindex_start(ctx, clean):
    """Start an Insight reindex.

    \b
    Examples:
    bender jira insight index reindex start
    bender jira insight index reindex start --clean
    """
    _params = None
    if clean:
        _params = {
            'clean': clean
        }
    jira_insight_index_reindex_path = 'rest/insight/1.0/index/reindex/start'
    _res = ctx.obj['connect'].post(jira_insight_index_reindex_path, params=_params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_insight_index_reindex.command('current-node')
@click.option('--clean/--no-clean', '-c', 'clean', default=False, is_flag=True, help='Clean before reindex.')
@click.pass_context
def cli_jira_insight_index_reindex_start(ctx, clean):
    """Start an Insight reindex on current-node.

    \b
    Examples:
    bender jira insight index reindex current-node
    bender jira insight index reindex current-node --clean
    """
    _params = None
    if clean:
        _params = {
            'clean': clean
        }
    jira_insight_index_reindex_current_node_path = 'rest/insight/1.0/index/reindex/currentnode'
    _res = ctx.obj['connect'].post(jira_insight_index_reindex_current_node_path, params=_params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_insight_index_reindex.command('object')
@click.option('--id', 'object_id', required=True, help='Object ID to reindex.')
@click.pass_context
def cli_jira_insight_index_reindex_object(ctx, object_id):
    """Start an Insight reindex on current-node.

    \b
    Examples:
    bender jira insight index reindex object --id 220
    """
    _params = None
    if object_id:
        _params = {
            'id': object_id
        }
    jira_insight_index_reindex_object_path = f'rest/insight/1.0/index/reindex/{object_id}'
    _res = ctx.obj['connect'].post(jira_insight_index_reindex_object_path, params=_params, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)

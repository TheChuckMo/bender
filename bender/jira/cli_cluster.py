import click

from bender.utils import json_headers


@click.group('cluster')
@click.pass_context
def jira_cluster(ctx):
    """Jira cluster.

    \b
    Examples:
    bender jira cluster state
    bender jira cluster nodes
    """
    pass


@jira_cluster.command('state')
@click.pass_context
def jira_cluster_state(ctx):
    """Jira cluster state.

    \b
    Examples:
    bender jira cluster state
    """
    jira_cluster_state_path = "/rest/api/2/cluster/zdu/state"
    _res = ctx.obj['connect'].get(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@jira_cluster.command('nodes')
@click.pass_context
def jira_cluster_nodes(ctx):
    """Jira cluster nodes.

    \b
    Examples:
    bender jira cluster nodes
    """
    jira_cluster_nodes_path = "/rest/api/2/cluster/nodes"
    _res = ctx.obj['connect'].get(jira_cluster_nodes_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)

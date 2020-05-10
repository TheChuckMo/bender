import click

from bender.utils import json_headers


@click.group('cluster')
@click.pass_context
def cli_jira_cluster(ctx):
    """Jira cluster.

    \b
    Examples:
    bender jira cluster state
    bender jira cluster node
    """
    pass


@cli_jira_cluster.command('state')
@click.pass_context
def cli_jira_cluster_state(ctx):
    """Jira cluster state.

    \b
    Examples:
    bender jira cluster state
    """
    jira_cluster_state_path = "rest/api/2/cluster/zdu/state"
    _res = ctx.obj['connect'].get(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster.group('upgrade')
@click.pass_context
def cli_jira_cluster_upgrade(ctx):
    """Manage Jira Cluster upgrade.

    \b
    Examples:
    bender jira cluster upgrade start
    bender jira cluster upgrade retry
    bender jira cluster upgrade cancel
    bender jira cluster upgrade approve
    """
    pass


@cli_jira_cluster_upgrade.command('start')
@click.confirmation_option(prompt='Start a cluster upgrade?')
@click.pass_context
def cli_jira_cluster_upgrade_start(ctx):
    """Put cluster in upgrade mode."""
    jira_cluster_state_path = "rest/api/2/cluster/zdu/start"
    _res = ctx.obj['connect'].post(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster_upgrade.command('approve')
@click.confirmation_option(prompt='Approve running upgrade?')
@click.pass_context
def cli_jira_cluster_upgrade_approve(ctx):
    """Approve upgrade to complete final tasks."""
    jira_cluster_state_path = "rest/api/2/cluster/zdu/approve"
    _res = ctx.obj['connect'].post(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster_upgrade.command('cancel')
@click.confirmation_option(prompt='Cancel running upgrade?')
@click.pass_context
def cli_jira_cluster_upgrade_cancel(ctx):
    """Cancel an active upgrade."""
    jira_cluster_state_path = "rest/api/2/cluster/zdu/cancel"
    _res = ctx.obj['connect'].post(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster_upgrade.command('retry')
@click.confirmation_option(prompt='Retry the upgrade?')
@click.pass_context
def cli_jira_cluster_upgrade_retry(ctx):
    """Retry upgrade steps."""
    jira_cluster_state_path = "rest/api/2/cluster/zdu/retry"
    _res = ctx.obj['connect'].post(jira_cluster_state_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster.group('node')
@click.pass_context
def cli_jira_cluster_node(ctx):
    """Jira cluster nodes.

    \b
    Examples:
    bender jira cluster nodes
    """
    pass


@cli_jira_cluster_node.command('state')
@click.pass_context
def cli_jira_cluster_node_state(ctx):
    """Jira cluster nodes.

    \b
    Examples:
    bender jira cluster nodes
    """
    jira_cluster_nodes_path = "rest/api/2/cluster/nodes"
    _res = ctx.obj['connect'].get(jira_cluster_nodes_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster_node.command('offline')
@click.confirmation_option(prompt='DANGER!!!! - Are you sure you want to offline a node?')
@click.argument('nodeid', type=str, required=True)
@click.pass_context
def cli_jira_cluster_node_offline(ctx, nodeid):
    """Make cluster node as offline.

    Probably shouldn't be used unless support suggests it or no other option.

    THIS IS DANGEROUS!
    """
    jira_cluster_node_offline_path = f'rest/api/2/cluster/node/{nodeid}/offline'
    click.echo('not yet implemented.')
    _res = ctx.obj['connect'].put(jira_cluster_node_offline_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_cluster_node.command('delete')
@click.argument('nodeid', type=str, required=True)
@click.confirmation_option(prompt='DANGER!!!! - Are you sure you want to delete a node?')
@click.pass_context
def cli_jira_cluster_node_delete(ctx, nodeid):
    """Delete node in cluster.

    Probably shouldn't be used unless support suggests it or no other option.

    THIS IS DANGEROUS!!!!
    """
    jira_cluster_node_delete_path = f'rest/api/2/cluster/node/{nodeid}'
    click.echo('not yet implemented.')
    _res = ctx.obj['connect'].delete(jira_cluster_node_delete_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)

import click

from bender import json_headers


@click.group('webhook')
@click.pass_context
def cli_jira_webhook(ctx):
    """Webhook management."""
    pass


@cli_jira_webhook.command('get')
@click.option('--id', 'webhook_id', default=None, type=str, help="id of webhook.")
@click.pass_context
def cli_jira_webhook_get(ctx, webhook_id):
    """Get all webhooks or by id.

    \b
    Examples:
    bender jira webhook get
    bender jira webhook get --id 2
    """
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    _url = jira_webhook_path

    if webhook_id:
        _url = f'{jira_webhook_path}/{webhook_id}'

    _res = ctx.obj['connect'].get(_url, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_webhook.command('add')
@click.pass_context
def cli_jira_webhook_add(ctx):
    """Add a webhook."""
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    click.echo('not yet implemented')


@cli_jira_webhook.command('delete')
@click.option('--id', 'webhook_id', required=True, default=None, type=str, help="id of webhook.")
@click.pass_context
def cli_jira_webhook_delete(ctx, webhook_id):
    """Delete webhook by id.

    \b
    Examples:
    bender jira webhook delete --id 4
    """
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    _url = f'{jira_webhook_path}/{webhook_id}'
    _res = ctx.obj['connect'].delete(_url, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)

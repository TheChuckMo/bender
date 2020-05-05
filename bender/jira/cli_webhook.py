import click

from bender.utils import json_headers, write_out


@click.group('webhook')
@click.pass_context
def jira_webhook(ctx):
    """Jira webhooks."""
    pass


@jira_webhook.command('get')
@click.option('--id', 'webhook_id', default=None, type=str, help="id of webhook.")
@click.pass_context
def jira_webhook_get(ctx, webhook_id):
    """get webhook."""
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    _url = jira_webhook_path

    if webhook_id:
        _url = f'{jira_webhook_path}/{webhook_id}'

    _res = ctx.obj['connect'].get(_url, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])


@jira_webhook.command('add')
@click.pass_context
def jira_webhook_add(ctx):
    """add a webhook."""
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    click.echo('not yet implemented')


@jira_webhook.command('delete')
@click.option('--id', 'webhook_id', required=True, default=None, type=str, help="id of webhook.")
@click.pass_context
def jira_webhook_delete(ctx, webhook_id):
    """delete a webhook by id."""
    jira_webhook_path = "rest/webhooks/1.0/webhook"
    _url = f'{jira_webhook_path}/{webhook_id}'
    _res = ctx.obj['connect'].delete(_url, headers=json_headers, auth=True)
    write_out(data=_res, output=ctx.obj['output'])

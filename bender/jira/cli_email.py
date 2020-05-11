import click

from bender import json_headers, form_headers, no_check_headers


@click.group('email')
@click.pass_context
def cli_jira_email(ctx):
    """Email processor and puller."""
    pass


@cli_jira_email.command('puller')
@click.argument('state', type=click.Choice(['on', 'off']), required=True)
@click.pass_context
def cli_jira_email_puller(ctx, state):
    """Set state of Jira email-puller.

    \b
    Examples:
    bender jira email puller on
    bender jira email puller off
    """
    jira_email_puller_path = f'rest/jira-email-processor-plugin/1.0/mail/global/puller/{state}'
    _res = ctx.obj['connect'].put(jira_email_puller_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)


@cli_jira_email.command('processor')
@click.argument('state', type=click.Choice(['on', 'off']), required=True)
@click.pass_context
def cli_jira_email_processor(ctx, state):
    """Set state of Jira email-processor.

    \b
    Examples:
    bender jira email processor on
    bender jira email processor off
    """
    jira_email_processor_path = f'rest/jira-email-processor-plugin/1.0/mail/global/processor/{state}'
    _res = ctx.obj['connect'].put(jira_email_processor_path, headers=json_headers, auth=True)
    ctx.obj['writer'].out(_res)
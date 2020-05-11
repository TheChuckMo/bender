import click


@click.group('upm')
@click.pass_context
def cli_jira_upm(ctx):
    """Universal Plugin Manager."""
    pass

import click
from .jira.cli import jira_cli
from .utils import config, config_file


# API paths
jira_status_path = "/status"
jira_settings_path = "/rest/api/2/settings"
jira_serverinfo_path = "/rest/api/2/serverInfo"
jira_application_properties_path = "/rest/api/2/application-properties"


@click.group('cli')
def cli():
    pass


@cli.command('config')
def cli_config():
    print('{}'.format(config_file))


cli.add_command(jira_cli)

